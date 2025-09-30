import argparse
import json
import os
import re
import sys 
from datetime import datetime
from math_construct.problems import get_problem_class, get_all_problem_classes
from math_construct.llm import DummyLLM, APIQuery, CoTSolver, CodeSolver
from config.meta_config import get_pydantic_models_from_path
from loguru import logger
from tqdm import tqdm

# Disable Langchain tracing
os.environ["LANGCHAIN_TRACING_V2"] = "false"

def get_output_length_assistant(query):
    length = 0
    for message in query:
        if message["role"] == "assistant":
            length += len(message["content"])
    return length

def result_to_string(result):
    end_string = ""
    for message in result:
        if message["role"] == "system":
            end_string += (30 * "=" + "System" + 30 * "=" + "\n")
            end_string += message["content"] + "\n"
        elif message["role"] == "user":
            end_string += (30 * "=" + "Query/Feedback" + 30 * "=" + "\n")
            end_string += message["content"] + "\n"
        else:
            end_string += (30 * "=" + "Response" + 30 * "=" + "\n")
            end_string += message["content"] + "\n"
    return end_string

def satisfies_tags(problem_inst, tags):
    if not tags:
        return True
    return any(tag in problem_inst.config.tags for tag in tags)

def distance(problem1, problem2):
    # for all parameters in problem1.config.parameters, calculate the distance between the values of the parameters if they are floats
    distance = 0
    for param in problem1.config.parameters:
        if isinstance(getattr(problem1, param), (float, int)):
            distance += abs(getattr(problem1, param) - getattr(problem2, param))
    return distance

def filter_problems(problems, n):
    if len(problems) <= n:
        logger.debug(f"Found {len(problems)} problems, returning all, for problem {problems[0].config.name}")
        solution_lengths = [len(problem.get_solution()) if isinstance(problem.get_solution(), (list, tuple)) else 0 for problem in problems]
        logger.debug(f"Selected problems with lengths: {solution_lengths}")
        return problems
    
    if problems[0].get_solution() is not None:
        solutions = [problem.get_solution() for problem in problems]
        solution_lengths = [len(solution) for solution in solutions]
        # sort by solution length, and select ::k problems
        sorted_indices = sorted(range(len(solution_lengths)), key=lambda k: solution_lengths[k])
        output_problems_indices = sorted_indices[::len(sorted_indices)//n]
        output_problems = [problems[i] for i in output_problems_indices][:n]
        logger.debug(f"Selected problems for {problems[0].config.name} with lengths: {[len(problem.get_solution()) for problem in output_problems]}")
        return output_problems

    logger.debug(f"No solutions found, using distance based selection for problem {problems[0].config.name}")
    # backup plan
    output_problems_indices = [0]
    while len(output_problems_indices) < n:
        max_distance = 0
        max_distance_index = 0
        for i, problem in enumerate(problems):
            if i in output_problems_indices:
                continue
            sumdistance = min([distance(problem, problems[j]) for j in output_problems_indices])
            if sumdistance > max_distance:
                max_distance = sumdistance
                max_distance_index = i
        output_problems_indices.append(max_distance_index)
    return [problems[i] for i in output_problems_indices]

def print_test_run(problem_class, problem_inst, result) -> None:
    logger.info(result_to_string(result))
    logger.info(30 * "=" + "Parameters" + 30 * "=")
    parameter_names = problem_inst.config.parameters
    parameter_values = [getattr(problem_inst, param) for param in parameter_names]
    logger.info({param: value for param, value in zip(parameter_names, parameter_values)})
    parsed_answer, is_correct, details = problem_inst.parse_and_check(result)
    logger.info(30 * "=" + "Parsed Answer" + 30 * "=")
    logger.info(parsed_answer)
    logger.info(30 * "=" + "Is Correct" + 30 * "=")
    logger.info(is_correct)
    logger.info(30 * "=" + "Details" + 30 * "=")
    logger.info(details)

def run(cfg, apis_restricted=None, models_restricted=None) -> None: 
    # New config = new run, set up the run dir and put the meta file  
    ts = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    logger.info(f"Current time: {ts}")
    run_dir = os.path.join("outputs", cfg.output_dir if cfg.output_dir is not None else ts)
    if not cfg.test_run:
        os.makedirs(run_dir, exist_ok=True)
        with open(f"{run_dir}/meta.json", "w") as f:
            json.dump({"ts": ts, "cfg": cfg.model_dump(mode="json")}, indent=4, fp=f)

    logger.info(f"Models: { cfg.models}")
    # Find the problems
    all_problems = get_all_problem_classes()

    matched_problems = []
    for problem in all_problems:
        # Any regex should match 
        for regex in cfg.problems:
            if re.search(regex, problem.config.name):
                matched_problems.append(problem)
                break

    if len(cfg.tags) > 0:
        matched_problems = [ci for ci in matched_problems if satisfies_tags(ci, cfg.tags)]

    logger.info(f"Matched problems: {[p.config.name for p in matched_problems]}")
    logger.info(f"Total matched problems: {len(matched_problems)}")

    # Generate problem instances and build the queries
    if cfg.input_dir_revisions is not None:
        json_input = json.load(open(cfg.input_dir_revisions, "r"))
        problem_classes_counts = dict()
        problem_instances = []
        for entry in json_input:
            problem_name = entry["config"]["name"]
            if problem_name not in problem_classes_counts:
                problem_classes_counts[problem_name] = 0
            problem_classes_counts[problem_name] += 1
            if problem_classes_counts[problem_name] > cfg.n_variations:
                continue
            problem_class = get_problem_class(problem_name)
            if problem_class is not None:
                problem_instance = problem_class.from_json(entry)
                problem_instances.append((problem_class, problem_instance))
    else:
        problem_instances = [] # (class, instance) pair
        for problem_class in tqdm(matched_problems):
            if cfg.n_try_variations is None:
                curr_instances = problem_class.generate_multiple(cfg.n_variations)
            else:
                curr_instances = filter_problems(problem_class.generate_multiple_explicit(cfg.n_try_variations), 
                                                 cfg.n_variations)
            for inst in curr_instances:
                    problem_instances.append((problem_class, inst))

    n_instances = dict()
    for p in problem_instances:
        n_instances[p[0].config.name] = n_instances.get(p[0].config.name, 0) + 1
    

    
    # Run the queries
    logger.info(f"Running {len(cfg.models)} models, each with {len(problem_instances)} queries")
    
    for model in cfg.models:
        api, model_name = model.split(":")[0], ":".join(model.split(":")[1:])
        if apis_restricted is not None and api not in apis_restricted:
            continue
        if models_restricted is not None and model_name not in models_restricted:
            continue

        problem_dumps = {}
        problem_instances_model = []
        for problem_class, problem_inst in problem_instances:
            add = True
            if os.path.exists(f"outputs/{cfg.output_dir}/{model_name.replace("/", "__")}/{problem_class.config.name}.json"):
                # load the json and check if we have enough instances
                json_input = json.load(open(f"outputs/{cfg.output_dir}/{model_name.replace("/", "__")}/{problem_class.config.name}.json", "r"))
                # load the problems from json
                problems_from_json = [(problem_class.from_json(entry["problem"]), entry) for entry in json_input]
                for problem in problems_from_json:
                    if problem[0] == problem_inst and get_output_length_assistant(problem[1]["response"]) > 0:
                        logger.info(f"Skipping problem {problem_class.config.name} as it already exists in the output directory")
                        if problem_class not in problem_dumps:
                            problem_dumps[problem_class] = []
                        problem_dumps[problem_class].append(problem[1])
                        add = False
                        break
            if add:
                problem_instances_model.append((problem_class, problem_inst))
                if problem_class not in problem_dumps:
                    problem_dumps[problem_class] = []
                problem_dumps[problem_class].append(None)

        querier = APIQuery(
            model=model_name,
            api=api,
            temperature=cfg.inference.temperature,
            top_p=cfg.inference.top_p,
            max_tokens=cfg.inference.max_tokens,
            concurrent_requests=cfg.inference.concurrent_requests,
            timeout=cfg.inference.timeout
        )
        if cfg.solver.type_solver == "code":
            solver = CodeSolver(
                querier=querier,
                system_prompt=cfg.solver.system_prompt,
                parse_feedback=cfg.solver.parse_feedback,
                check_feedback=cfg.solver.check_feedback,
                max_feedback_rounds=cfg.solver.max_feedback_rounds,
                formatting_prefix=cfg.solver.formatting_prefix,
                error_string=cfg.solver.error_string,
                image_name=cfg.solver.image_name,
                timeout=cfg.solver.timeout,
                cpus=cfg.solver.cpus,
                memory=cfg.solver.memory,
                n_parallel_code_executions=cfg.solver.n_parallel_code_executions,
                max_code_iterations=cfg.solver.max_code_iterations,
                code_feedback_prompt=cfg.solver.code_feedback_prompt,
                stop_at_timeout=cfg.solver.stop_at_timeout,
                give_solution=cfg.solver.give_solution,
            )
        else:
            solver = CoTSolver(
                querier=querier,
                system_prompt=cfg.solver.system_prompt,
                parse_feedback=cfg.solver.parse_feedback,
                check_feedback=cfg.solver.check_feedback,
                max_feedback_rounds=cfg.solver.max_feedback_rounds,
                formatting_prefix=cfg.solver.formatting_prefix,
                error_string=cfg.solver.error_string,
                give_solution=cfg.solver.give_solution,
            )

        # Process problems in batches
        batch_size = cfg.solver.batch_size if hasattr(cfg.solver, 'batch_size') else 10

        model_dir = os.path.join(run_dir, model_name.replace("/", "__"))
        os.makedirs(model_dir, exist_ok=True)

        for batch_start in range(0, len(problem_instances_model), batch_size):
            batch_end = min(batch_start + batch_size, len(problem_instances_model))
            batch = problem_instances_model[batch_start:batch_end]
            
            logger.info(f"Processing batch {batch_start//batch_size + 1}, problems {batch_start+1} to {batch_end}")
            results, detailed_costs = solver.solve([ci[1] for ci in batch])

            # If test run only do some quick logging
            if cfg.test_run:
                for ci, result in zip(batch, results):
                    problem_class, problem_inst = ci
                    print_test_run(problem_class, problem_inst, result)
                continue

            # Process and store results for this batch
            for ci, result, cost in zip(batch, results, detailed_costs):
                problem_class, problem_inst = ci
                if problem_class not in problem_dumps:
                    problem_dumps[problem_class] = []
                # remove the input query and system message from the response
                if result[0]['role'] == "system":
                    result = result[1:]
                result = result[1:]
                dump = {
                    "problem": problem_inst.to_json(),
                    "response": result,
                    "cost": cost
                }
                # loop through problem dumps and first the first None, then set it to dump
                for i, d in enumerate(problem_dumps[problem_class]):
                    if d is None:
                        problem_dumps[problem_class][i] = dump
                        break

                # If we completed a class, save the results
                if all(d is not None for d in problem_dumps[problem_class]):
                    dumps = problem_dumps[problem_class]
                    problem_path = os.path.join(model_dir, f"{problem_class.config.name}.json")
                    with open(problem_path, "w") as f: 
                        json.dump(dumps, f, indent=4)
                    print(f"Finished and saved:", problem_path)

        logger.info("Run finished")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run the math construct pipeline")
    parser.add_argument("config", type=str, help="Path to the config file")
    parser.add_argument("--apis", type=str, nargs="+", default=None, help="Restrict APIs to run on")
    parser.add_argument("--models", type=str, nargs="+", default=None, help="Restrict models to run on")

    args = parser.parse_args()
    cfg = get_pydantic_models_from_path(args.config)[0]
    logger.info(f"Running config: {cfg}")
    with logger.catch(reraise=True):
        run(cfg, apis_restricted=args.apis, models_restricted=args.models)
