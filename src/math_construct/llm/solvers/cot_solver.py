from .solver import Solver
import logging
from loguru import logger
import numpy as np

class CoTSolver(Solver):
    def __init__(self, 
                 querier, 
                 system_prompt: str = None, 
                 parse_feedback: bool = False,
                 check_feedback: bool = False, 
                 max_feedback_rounds: int = 1,
                 formatting_prefix: str = "Format your reply as follows:",
                 give_solution: bool = False,
                 stop_at_timeout: bool = False,
                 error_string: str = r"The solution parser encountered the following error:\n{error}\nPlease format your reply accurately."):
        """
        Initializes the CoTSolver with the given parameters.

        Args:
            querier: The querier object used for querying the model.
            system_prompt (str, optional): The system prompt to be used. Defaults to None.
            parse_feedback (bool, optional): Flag to enable parsing feedback. Defaults to False.
            check_feedback (bool, optional): Flag to enable checking feedback. Defaults to False.
            max_feedback_rounds (int, optional): Maximum number of feedback rounds. Defaults to 1.
            formatting_prefix (str, optional): Prefix for formatting instructions. Defaults to "Format your reply as follows:".
            give_solution (bool, optional): Flag to enable giving the solution to do sanity parsing checks. Defaults to False.
            error_string (str, optional): Error message template with a placeholder for the error. Defaults to r"The solution parser encountered the following error:\n{error}\nPlease format your reply accurately.".

        Raises:
            AssertionError: If `parse_feedback` or `check_feedback` is True and `error_string` does not contain the placeholder {error}.
        """
        if parse_feedback or check_feedback:
            assert "{error}" in error_string, "Error string must contain the placeholder {error}"
        super().__init__(querier)
        self.system_prompt = system_prompt
        self.parse_feedback = parse_feedback
        self.check_feedback = check_feedback
        self.max_feedback_rounds = max_feedback_rounds
        self.formatting_prefix = formatting_prefix
        self.error_string = error_string
        self.give_solution = give_solution
        self.stop_at_timeout = stop_at_timeout

    def build_query(self, problem):
        """
        Constructs an initial query message for the given problem.

        Args:
            problem (object): The problem instance to build the query for. It should have a  method and a 
                              get_formatting_instructions method.

        Returns:
            list: A list of message dictionaries formatted for the query. The list includes a system prompt if 
                  provided, followed by the user prompt containing the problem description and formatting instructions.
        """
        prompt = str(problem)
        prompt += f"\n\n{self.formatting_prefix}\n{problem.get_formatting()}"
        if self.give_solution:
            prompt += f"\n\nYou are given the solution to the problem: {problem.get_solution()}"
        messages = []
        if self.system_prompt is not None: 
            messages.append({"role": "system", "content": self.system_prompt})
        messages.append({"role": "user", "content": prompt})
        return messages
    
    def check_timeout(self, query) -> bool:
        # we exclude the last message to give the model a chance to respond
        if any(f"TimeOutError: exceeded {self.timeout} seconds timeout." in response["content"] for response in query):
            return True
        return False
    
    def remove_timeouts(self, queries, code_indices):
        new_code_indices = []
        for i in code_indices:
            if not self.check_timeout(queries[i]):
                new_code_indices.append(i)
        return new_code_indices

    def build_queries(self, problems):
        """
        Build a list of queries from a list of problems.

        Args:
            problems (list): A list of problem instances.

        Returns:
            list: A list of queries generated from the given problems.
        """
        queries = []
        for problem in problems:
            queries.append(self.build_query(problem))
        return queries
    
    def add_response(self, query, response):
        if isinstance(response, tuple) and response[0] is None:
            query.append({"role": "api_error", "content": str(response[1])})
        elif isinstance(response, str):
            query.append({"role": "assistant", "content": response})
        else:
            query.extend(response)
        return query
    
    def is_valid_trace(self, query):
        return not any(m["role"] == "api_error" for m in query)
    
    def build_parse_feedback_query(self, problem, current_messages, 
                                   current_parsed_response=None, iteration=None):
        """
        Builds and parses a feedback query for a given problem based on the current messages and iteration.
        Args:
            problem (object): The problem instance that provides parsing and checking methods.
            current_messages (list): The list of current messages exchanged.
            current_parsed_response (optional): The current parsed response, if any. Defaults to None.
            iteration (optional): The current iteration information, if any. Defaults to None.
        Returns:
            tuple: A tuple containing:
                - new_messages (list or None): The updated list of messages with feedback appended, or None if no feedback is needed.
                - parsed_response (object or None): The parsed response from the problem, or None if an error occurred or no parsing was done.
        """
        if (iteration is not None and iteration["feedback"] >= self.max_feedback_rounds) or \
            not self.is_valid_trace(current_messages):
            return None, current_parsed_response
        try:
            if self.check_feedback:
                parsed_response, is_correct, error = problem.parse_and_check(current_messages)
            else:
                parsed_response = problem.parse(current_messages)
                is_correct = True
                error = None
        except Exception as e:
            parsed_response = None
            error = str(e)
        
        # Model does not need feedback anymore
        if error is None or (self.check_feedback and is_correct):
            return None, parsed_response

        feedback = self.error_string.format(error=error)
        feedback += f"\n\n{self.formatting_prefix}\n{problem.get_formatting()}"
    
        new_messages = current_messages.copy()
        new_messages.append({"role": "user", "content": feedback})

        return new_messages, parsed_response
    
    def build_parse_feedback_queries(self, problems, queries, parsed_responses, iterations=None):
        """
        Builds and parses feedback queries for a list of problems.

        Args:
            problems (list): A list of problems to generate feedback queries for.
            queries (list): A list of current messages or queries associated with each problem.
            parsed_responses (list): A list of parsed responses corresponding to each problem.
            iterations (list, optional): A list of iteration counts for each problem. Defaults to None.

        Returns:
            tuple: A tuple containing two lists:
                - queries_new (list): A list of new queries generated for each problem.
                - parsed_responses_new (list): A list of new parsed responses corresponding to each problem.
        """
        if iterations is None:
            iterations = [None for _ in range(len(problems))]
        queries_new = []
        parsed_responses_new = []
        for problem, current_messages, parsed_response, iteration in zip(problems, queries, 
                                                                         parsed_responses, iterations):
            query, parsed_response = self.build_parse_feedback_query(problem, 
                                                                     current_messages,
                                                                     parsed_response, 
                                                                     iteration)
            queries_new.append(query)
            parsed_responses_new.append(parsed_response)
        return queries_new, parsed_responses_new
    
    def solve_initial_round(self, problems):
        """
        Solves the initial round of problems by building queries, running them, and appending responses.

        Args:
            problems (list): A list of problems to be solved.

        Returns:
            list: A list of queries with appended responses from the assistant.
        """
        logger.info("Performing initial round.")
        queries = self.build_queries(problems)
        responses, detailed_cost, cost = self.querier.run_queries(queries)
        self.cost += cost["cost"]
        for i in range(len(queries)):
            queries[i] = self.add_response(queries[i], responses[i])
            self.detailed_cost[i]["cost"] += detailed_cost[i]["cost"]
            self.detailed_cost[i]["input_tokens"] += detailed_cost[i]["input_tokens"] 
            self.detailed_cost[i]["output_tokens"] += detailed_cost[i]["output_tokens"]
        logger.info("Initial round done.")
        return queries
    
    def solve_parse_feedback_round(self, problems, queries, parsed_responses, iterations=None):
        """
        Executes a round of parsing feedback for a given set of problems and queries.

        This method builds feedback queries based on the provided problems, queries, and parsed responses.
        It then runs these queries asynchronously and updates the original queries with the responses.

        Args:
            problems (list): A list of problems to be solved.
            queries (list): A list of queries corresponding to the problems.
            parsed_responses (list): A list of parsed responses from previous iterations.
            iterations (int, optional): The number of iterations to run. Defaults to None.

        Returns:
            tuple: A tuple containing the updated queries and parsed responses.
        """
        logger.info("Performing feedback round")
        queries_here, parsed_responses = self.build_parse_feedback_queries(problems, 
                                                                            queries,
                                                                            parsed_responses,
                                                                            iterations)
        queries_not_none_indices = [i for i, q in enumerate(queries_here) if q is not None]
        if self.stop_at_timeout:
            queries_not_none_indices = self.remove_timeouts(queries_here, queries_not_none_indices)
        queries_not_none = [queries_here[i] for i in queries_not_none_indices]
        responses, detailed_cost, cost = self.querier.run_queries(queries_not_none)
        self.cost += cost["cost"]
        for i, response, detail in zip(queries_not_none_indices, responses, detailed_cost):
            queries[i].append(queries_here[i][-1])
            queries[i] = self.add_response(queries[i], response)
            self.detailed_cost[i]["cost"] += detail["cost"]
            self.detailed_cost[i]["input_tokens"] += detail["input_tokens"] 
            self.detailed_cost[i]["output_tokens"] += detail["output_tokens"]
        logger.info("Feedback round done.")
        return queries, parsed_responses
    
    def solve_parse_feedback_rounds(self, problems, queries):
        """
        Solves problems through multiple feedback rounds, parsing responses at each round.

        Args:
            problems (list): A list of problems to be solved.
            queries (list): A list of initial queries corresponding to the problems.

        Returns:
            list: The final list of queries after processing through feedback rounds.
        """
        if self.parse_feedback or self.check_feedback:
            parsed_responses = [None for _ in range(len(problems))]
            for _ in range(self.max_feedback_rounds):
                queries, parsed_responses = self.solve_parse_feedback_round(problems, 
                                                                            queries, 
                                                                            parsed_responses)
                checker = [problem.parse_and_check(q) for problem, q in zip(problems, queries)]
                logger.info(f"Solved instances after feedback round: {np.mean([c[1] for c in checker]):.5f}")
        return queries

    def solve(self, problems):
        """
        Solves the given problems by performing an initial round of solving and then
        parsing feedback rounds.

        Args:
            problems (list): A list of problems to be solved.

        Returns:
            list: A list of queries after solving and parsing feedback rounds.
        """
        self.cost = 0
        self.detailed_cost = [{
            "cost": 0,
            "input_tokens": 0,
            "output_tokens": 0,
        } for _ in range(len(problems))]
        queries = self.solve_initial_round(problems)
        checker = [problem.parse_and_check(q) for problem, q in zip(problems, queries)]
        logger.info(f"Solved instances after feedback round: {np.mean([c[1] for c in checker]):.5f}")
        queries = self.solve_parse_feedback_rounds(problems, queries)
        # log cost
        logger.info(f"Total cost: {self.cost}")
        return queries, self.detailed_cost
