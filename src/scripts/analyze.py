import argparse
import json
import os
import re
import time 
import sys
from math_construct.problems import get_all_problem_classes
from math_construct.problems.problem import CheckerTag
from loguru import logger

# TODO figure out if problem is the original and separate metrics

# Analyze (parse,check,aggregate) a run from outputs/ or logs/ with optional whitelists
def analyze_run(run_dir, models_whitelist=None, problems_whitelist=None, no_parser=False, stop_timeout=False, 
                max_variations=4, lengthstudy=False, tokensstudy=False):
    # Prepare problem classes
    problem_classes = get_all_problem_classes()
    problem_classes = {problem_class.config.name: problem_class for problem_class in problem_classes}

    # Find all models
    models = [f for f in os.listdir(run_dir) if os.path.isdir(os.path.join(run_dir, f))]
    if models_whitelist is not None:
        models = [m for m in models if m in models_whitelist]

    # Collect timings to find outliers
    parsecheck_durations = {}

    # Go through models and collect results 
    results = {} 
    for model in models:
        logger.info(f"========== Model: {model}")
        results[model] = {}
        model_dir = os.path.join(run_dir, model)
        # Find all jsons which are problems 
        problem_names = [f[:-5] for f in os.listdir(model_dir) if f.endswith(".json")]
        if problems_whitelist is not None:
            filtered_problem_names = [] 
            for p in problem_names:
                for regex in problems_whitelist:
                    if re.search(regex, p):
                        filtered_problem_names.append(p)
                        break
            problem_names = filtered_problem_names
        problem_names = sorted(problem_names)

        # Go through problems
        for problem_name in problem_names:
            results[model][problem_name] = []
            if problem_name not in problem_classes:
                logger.warning(f"Problem {problem_name} not found in problem classes")
                continue
            problem_class = problem_classes[problem_name]
            with open(os.path.join(model_dir, f'{problem_name}.json'), "r") as f:
                instances_json = json.load(f)
            
            if len(instances_json) > max_variations:
                instances_json = instances_json[:max_variations]

            for i, entry in enumerate(instances_json): 
                # Load data for this problem instance
                try:
                    instance = problem_class.from_json(entry["problem"])
                except Exception as e:
                    logger.debug(f"Error parsing an instance of the problem {problem_name}: {e}")
                    continue
                response = entry["response"]
                if type(response) == list and not isinstance(response[0], dict):
                    response = "\n\n".join(response)
                if no_parser or stop_timeout:
                    actual_response = []
                    for message in response:
                        if no_parser and message["role"] == "user" and "The solution parser encountered the following error:" in message["content"]:
                            break
                        if stop_timeout and message["role"] == "user" and "TimeOutError: exceeded " in message["content"]:
                            break
                        actual_response.append(message)
                    response = actual_response

                param_values = entry['problem']['param_values']
                orig_param_values = entry['problem']['config']['original_parameters']
                logger.debug(f"Problem: {problem_name}")

                # Parse and check
                # start timer 
                ts_start = time.time()
                answer, is_correct, details = instance.parse_and_check(response)

                if is_correct and not details.startswith("CheckerTag.CORRECT"):
                    raise ValueError(f"Answer is correct but details are {details}")
                
                type_error = parse_solution_errors(details, response)

                ts_end = time.time()
                parsecheck_duration = ts_end - ts_start
                parsecheck_durations[f"{model}/{problem_name}/{i}"] = parsecheck_duration

                instance_result = entry.copy()
                instance_result['answer'] = answer
                instance_result['is_correct'] = is_correct
                instance_result['parsecheck_details'] = details
                instance_result["cost"] = entry["cost"]["cost"]
                instance_result["output_tokens"] = entry["cost"].get("output_tokens", -1)
                instance_result["type_error"] = type_error
                results[model][problem_name].append(instance_result)
    
    if tokensstudy:
        tokens = {}
        for model in models:
            tokens[model + "-correct"] = []
            tokens[model + "-wrong"] = []
            for problem_name in results[model].keys():
                for instance in results[model][problem_name]:
                    print(instance["output_tokens"], instance["is_correct"])
                    if instance["is_correct"]:
                        tokens[model + "-correct"].append(instance["output_tokens"])
                    else:
                        tokens[model + "-wrong"].append(instance["output_tokens"])
        # store the object
        json.dump(tokens, open("data/tokens.json", "w"), indent=4)
        
    model_results = dict()
    # Print statistics
    for model in models:
        logger.info(f"Model: {model}")
        res = results[model] 
        if len(res) == 0:
            continue 
        accs = []
        accs_all = []
        costs = []
        error_types = dict()
        detailed_results = []

        for problem_name in list(problem_classes.keys()):
            if len(res.get(problem_name, [])) == 0:
                continue
            logger.debug(f"    Problem: {problem_name}")
            corrects = [inst['is_correct'] for inst in res[problem_name]]
            nb_inst = len(corrects)
            acc = sum(corrects) / nb_inst 
            logger.debug(f"        accuracy: {acc} ({nb_inst} instances)")
            accs.append(acc)
            costs.append(sum([inst["cost"] for inst in res[problem_name]]))
            accs_all.append(all(corrects))
            for inst in res[problem_name]:
                error_types[inst["type_error"]] = error_types.get(inst["type_error"], 0) + 1 / nb_inst
                detailed_results.append({
                    "correct": inst["is_correct"],
                    "error": inst["type_error"],
                    "cost": inst["cost"],
                    "problem_name": problem_name,
                    "variation_parameters": inst["problem"]["param_values"]
                })
        avg_acc = sum(accs) / len(accs)
        all_errors_sum = sum(error_types.values())
        normalized_error_types = {k: v / all_errors_sum for k, v in error_types.items()}
        tot_variations = sum([len(res[problem_name]) for problem_name in res.keys()])
        logger.info(f"    avg accuracy: {100 * avg_acc:.4f} ({len(accs)} problems, {tot_variations} variations)")
        # print cost
        logger.info(f"    sum cost: {sum(costs):.4f}")
        logger.info(f"    all correct: {100 * sum(accs_all) / len(accs_all):.4f} ({len(accs_all)} problems)")
        logger.info(f"    error types:")


        for k, v in normalized_error_types.items():
            logger.info(f"        {k}: {100 * v:.4f}")
        
        model_results[model] = {
            "avg_acc": avg_acc,
            "avg_cost": sum(costs),
            "all_correct": sum(accs_all) / len(accs_all),
            "error_types": normalized_error_types,
            "detailed_results": detailed_results
        }
    # Optionally print timings 
    # Sorted 
    sorted_durations = sorted(parsecheck_durations.items(), key=lambda x: x[1], reverse=True)
    sorted_durations = [f"{k}: {t:0.4f}s" for k, t in sorted_durations]
    #logger.info("Parse and check durations:")
    #for d in sorted_durations:
    #    logger.info(d)
    if lengthstudy:
        print(f"Problem names: {problem_names}")
        # dirty, save a bit of a different txt 
        with open("logs/lengthstudy/data.txt", "w") as f:
            for problem_name in problem_names:
                print(problem_name)
                f.write(f"{problem_name}\n")
                for i in range(max_variations):
                    chek = set()
                    if i >= len(results[models[0]].get(problem_name, [])):
                        continue
                    for model in models:
                        chek.add(str(results[model][problem_name][i]["problem"]["param_values"]))
                    assert(len(chek) == 1)

                    try:
                        problem_class = problem_classes[problem_name]
                        instance_result = results[models[0]][problem_name][i]
                        instance = problem_class.from_json(instance_result["problem"])
                    except Exception as e:
                        print(e)
                    parameter_names = instance.config.parameters
                    parameter_values = [getattr(instance, param) for param in parameter_names]
                    params = "/".join(f"{k}={v}" for k, v in zip(parameter_names, parameter_values))

                    sol = instance.get_solution()
                    sol_ok = int(instance.check_raw(sol))
                    s = f"variant::{params},len::{len(str(sol))},getsol::{sol_ok}"
                    for model in models:
                        instance_result = results[model][problem_name][i]
                        ok = instance_result["is_correct"]
                        if "gemini" in model:
                            s += f",gemini-cot::{int(ok)}"
                        if "claude" in model:
                            s += f",claude-bf::{int(ok)}"
                    f.write(s + "\n")

    #logger.info(results)
    return results, model_results

def get_output_length_assistant(query):
    length = 0
    for message in query:
        if message["role"] == "assistant":
            length += len(message["content"])
    return length

def parse_solution_errors(details, query):
    if r"Error parsing solution: No \boxed content found" in details:
        type_error = "No Boxed Answer"
    elif "Error parsing solution:" in details:
        if ", but got" in details:
            details = details.split(", but got")[1]
        if "solution" in details.lower() or "no " in details.lower() or "exist" in details.lower() or "not" in details.lower():
            type_error = "Model says no solution exists"
        else:
            type_error = "Error parsing solution"
    elif ":" in details:
        type_error = details.split(":")[0]
    else:
        type_error = details
    if type_error == "Parser returned None":
        if get_output_length_assistant(query) == 0:
            return "No Boxed Answer"
        else:
            return "Error parsing solution"
    if type_error == "Error checking solution":
        return "CheckerTag.INCORRECT_FORMAT"
    return type_error

def error_type_latex(error_type_dict):
    result = ""
    for possible_error in ["CheckerTag.CORRECT", "CheckerTag.INCORRECT_SOLUTION", "CheckerTag.INCORRECT_FORMAT", "CheckerTag.INCORRECT_LENGTH", "No Boxed Answer", "Model says no solution exists", "Error parsing solution"]:
        result += f"{error_type_dict.get(possible_error, 0) * 100:.4f} &"
    return result[:-1] + r"\\"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", type=str, nargs="+", required=True, help="List of runs to analyze")
    parser.add_argument("--models", type=str, nargs="+", default=None, help="Restricted list of models to analyze")
    parser.add_argument("--problems", type=str, nargs="+", default=None, help="Restricted list of problems to analyze")
    parser.add_argument("--only-info", action="store_true", help="Only print info logs and not debug logs.")
    parser.add_argument("--no-parser", action="store_true", help="Stops model output before parser feedback, useful only for our paper results.")
    parser.add_argument("--latex", action="store_true", help="Prints results in latex format")
    parser.add_argument("--store-file", type=str, default="data/results.json", help="File to store results")
    parser.add_argument("--reload", action="store_true", help="Reloads the results file")
    parser.add_argument("--stop-timeout", action="store_true", help="Stops model output before timeout feedback, useful only for our paper results.")
    parser.add_argument("--max-variations", type=int, default=4, help="Maximum number of variations to consider in the statistics, useful only for our paper results.")
    parser.add_argument("--no-cost", action="store_true", help="Do not print cost in the latex results")
    parser.add_argument("--lengthstudy", action="store_true", help="Tmp flag for diff output processing")
    parser.add_argument("--tokensstudy", action="store_true", help="Tmp flag for tokens study")
    args = parser.parse_args()
    if args.only_info:
        logger.remove()
        logger.add(sys.stdout, level="INFO")

    runs_results = []
    if args.reload and os.path.exists(args.store_file):
        runs_results = json.load(open(args.store_file, "r"))
    
    for run in args.run:
        if any([run == r["name"] for r in runs_results]):
            continue
        results, model_results = analyze_run(run, args.models, args.problems, args.no_parser, args.stop_timeout, args.max_variations, args.lengthstudy, args.tokensstudy)
        runs_results.append({"name": run, "model_results": model_results})

    all_models = set()
    for run_result in runs_results:
        all_models.update(run_result["model_results"].keys())

    if args.store_file is not None:
        with open(args.store_file, "w") as f:
            json.dump(runs_results, f, indent=4)
    
    if args.latex:
        print("MAIN")
        for model in all_models:
            latex_results = f"{model} &"
            for run_results in runs_results:
                if model in run_results["model_results"]:
                    res = run_results["model_results"][model]
                    if args.no_cost:
                        latex_results += f" {res['avg_acc'] * 100:.4f} & {res['all_correct'] * 100:.4f} &"
                    else:
                        latex_results += f" {res['avg_acc'] * 100:.4f} & {res['all_correct'] * 100:.4f}  & {res['avg_cost']:.4f} &"
                else:
                    if args.no_cost:
                        latex_results += " {-} & {-} &"
                    else:
                        latex_results += " {-} & {-} & {-} &"
            latex_results = latex_results[:-1] + r"\\"
            print(latex_results)
        print("ERRORS")
        for model in all_models:
            for i, results_run in enumerate(runs_results):
                if model in results_run["model_results"]:
                    print(f"{model} ({i}) & {error_type_latex(results_run['model_results'][model]['error_types'])}")
