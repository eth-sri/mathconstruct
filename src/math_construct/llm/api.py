from .llm_costs import llm_costs
from loguru import logger
import re
import os
from tqdm import tqdm
from google import genai
from openai import OpenAI
import anthropic
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

class APIQuery:
    def __init__(self, model, 
                 timeout=500, 
                 temperature=0, 
                 max_tokens=256,
                 api='openai', 
                 max_retries=5,
                 concurrent_requests=10, 
                 is_chat=True,
                 no_system_messages=False,
                 read_cost=1,  
                 write_cost=1,
                 sleep_on_error=60,
                 sleep_after_request=0.1,
                 throw_error_on_failure=False,
                 max_tokens_param="max_tokens", 
                 reasoning_effort=None,
                 **kwargs):
        """
        Initializes an instance of the API class.
        Args:
            model (str): The model to query.
            timeout (int, optional): The timeout value in seconds. Defaults to 30.
            temperature (int, optional): The temperature value. Defaults to 0.
            max_tokens (int, optional): The maximum number of tokens. Defaults to 256.
            return_logprobs (bool, optional): Whether to return log probabilities. Defaults to False.
            api (str, optional): The API to be used, one of "openai", "together", "huggingface", "google", "claude", "hyperbolic", "sambanova". Defaults to 'openai'.
            chat (bool, optional): Whether to enable chat mode. Defaults to True.
            max_retries (int, optional): The maximum number of retries. Defaults to 20.
            concurrent_requests (int, optional): The number of concurrent requests. Defaults to 30.
            check_every_n_seconds (float, optional): The interval for checking rate limits. Defaults to 0.1.
            read_cost (float, optional): The cost of read operations. Defaults to None.
            write_cost (float, optional): The cost of write operations. Defaults to None.
            throw_error_on_failure (bool, optional): Whether to throw an error on too many failures or just return None. Defaults to False.
            **kwargs: Additional keyword arguments for the API model (e.g., top_p, top_k, ...).
        Returns:
            None
        """
        self.openai_responses = ("gpt-5" in model)

        if "think" in model and api == "google":
            is_chat = False # think model cannot handle chat
            max_tokens_param = "max_output_tokens"
        if ("o1" in model or "o3" in model or "gpt-5" in model) and api == "openai":
            no_system_messages = True # o1 model cannot handle system messages
            if not self.openai_responses:
                max_tokens_param = "max_completion_tokens"
            else:
                max_tokens_param = "max_output_tokens"
            if "top_p" in kwargs:
                del kwargs["top_p"]
            if "top_k" in kwargs:
                del kwargs["top_k"]
            if "--" in model:
                model, reasoning_effort = model.split("--")
        if api == "anthropic" and max_tokens is not None:
            max_tokens = min(8192, max_tokens)
        if api == "deepseek" and max_tokens is not None:
            max_tokens = min(8192, max_tokens)
        

        self.model = model
        self.temperature = temperature
        self.kwargs = kwargs
        if max_tokens is not None:
            self.kwargs[max_tokens_param] = max_tokens
        if reasoning_effort is not None:
            if not self.openai_responses:
                self.kwargs["reasoning_effort"] = reasoning_effort
            else:
                self.kwargs["reasoning"] = {"effort": reasoning_effort, "summary": "auto"}

        self.timeout = timeout
        self.max_retries = max_retries
        self.throw_error_on_failure = throw_error_on_failure
        self.concurrent_requests = concurrent_requests
        self.is_chat = is_chat
        self.no_system_messages = no_system_messages
        self.sleep_on_error = sleep_on_error
        self.sleep_after_request = sleep_after_request
        self.max_tokens_param = max_tokens_param

        self.api = api
        self.api_key = None
        self.base_url = None

        self.initialize_api_keys()
        self.initialize_read_write_costs(model, read_cost, write_cost)

    def initialize_read_write_costs(self, model, read_cost, write_cost):
        if read_cost is None or read_cost == 1:
            current_matched_string = None
            for model_regex, costs in llm_costs.items():
                if re.match(model_regex, model):
                    if current_matched_string is None or len(model_regex) > len(current_matched_string):
                        current_matched_string = model_regex
                        if isinstance(costs, tuple):
                            self.read_cost, self.write_cost = costs
                        else:
                            self.read_cost, self.write_cost = costs, costs
            if current_matched_string is not None:
                logger.info(f"Using read cost {self.read_cost} and write cost {self.write_cost} for model {model} from regex {current_matched_string}")
            else:
                self.read_cost = 1
                self.write_cost = 1
                logger.info(f"Using default read cost {self.read_cost} and write cost {self.write_cost} for model {model}")
        else:
            self.read_cost = read_cost
            self.write_cost = write_cost

    def initialize_api_keys(self):
        if self.api == "openai":
            self.api_key = os.getenv("OPENAI_API_KEY")
        elif self.api == "together":
            self.api_key = os.getenv("TOGETHER_API_KEY")
            self.base_url = "https://api.together.xyz/v1"
            self.api = "openai"
        elif self.api == "google":
            self.api_key = os.getenv("GOOGLE_API_KEY")
            if not "think" in self.model:
                self.api = "openai"
                self.base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
        elif self.api == "anthropic":
            self.api_key = os.getenv("ANTHROPIC_API_KEY")
        elif self.api == "hyperbolic":
            self.api_key = os.getenv("HYPERBOLIC_API_KEY")
            self.base_url = "https://api.hyperbolic.xyz/v1"
            self.api = "openai"
        elif self.api == 'sambanova':
            self.api_key = os.getenv("SAMBA_API_KEY")
            self.base_url = "https://api.sambanova.ai/v1"
            self.api = "openai"
        elif self.api == "deepseek":
            self.api_key = os.getenv("DEEPSEEK_API_KEY")
            self.base_url = "https://api.deepseek.com"
            self.api = "openai"
        elif self.api == "openrouter":
            self.api_key = os.getenv("OPENROUTER_API_KEY")
            self.base_url = "https://openrouter.ai/api/v1"
            self.api = "openai"
        else:
            raise ValueError(f"API {self.api} not supported.")
        assert self.api_key is not None, f"API key not found."

    def prepare_query(self, query):
        if not self.is_chat:
            output_query = query[0]["content"]
            for message in query:
                output_query += f"\n\n{'=' * 20}{message['role']}{'=' * 20}\n\n{message['content']}"
            return output_query
        elif self.no_system_messages:
            # convert system role to user role
            query = [{
                "role": message["role"] if message["role"] != "system" else "developer",
                "content": message["content"]
            } for message in query]
        return query
    
    def get_cost(self, response):
        cost = response["input_tokens"] * self.read_cost + response["output_tokens"] * self.write_cost
        return cost / (10 ** 6)

    def run_queries(self, queries):
        logger.info(f"Running {len(queries)} queries with {self.concurrent_requests} requests.")
        with ThreadPoolExecutor(max_workers=self.concurrent_requests) as executor:
            future_to_index = {
                executor.submit(self.run_query_with_retry, query): i
                for i, query in enumerate(queries)
            }

            results = [None] * len(queries)

            for future in tqdm(as_completed(future_to_index), total=len(future_to_index)):
                i = future_to_index[future]
                results[i] = future.result()
        detailed_cost = [
            {
                "cost": self.get_cost(result),
                "input_tokens": result["input_tokens"],
                "output_tokens": result["output_tokens"],
            }
            for result in results
        ]
        cost = {
            "cost": sum([d["cost"] for d in detailed_cost]),
            "input_tokens": sum([d["input_tokens"] for d in detailed_cost]),
            "output_tokens": sum([d["output_tokens"] for d in detailed_cost]),
        }
        return [result['output'] for result in results], detailed_cost, cost
    
    def run_query_with_retry(self, query):
        i = 0
        while i < self.max_retries:
            try:
                output = self.run_query(query)
                time.sleep(self.sleep_after_request)
                return output
            except Exception as e:
                logger.error(f"Error: {e}")
                time.sleep(self.sleep_on_error)
                # if api error is not due to rate limit, try again
                if "rate limit" not in str(e).lower() and "429" not in str(e):
                    i += 1
                continue
        if self.throw_error_on_failure:
            raise ValueError("Max retries reached.")
        else:
            return {
                "output": "",
                "input_tokens": 0,
                "output_tokens": 0,
            }
    
    def run_query(self, query):
        query = self.prepare_query(query)
        if self.api == "openai":
            if self.openai_responses:
                return self.openai_responses_query(query)
            else:
                return self.openai_query(query)
        elif self.api == "together":
            return self.together_query(query)
        elif self.api == "google":
            return self.google_query(query)
        elif self.api == "anthropic":
            return self.anthropic_query(query)
        
    def anthropic_query(self, query):
        client = anthropic.Anthropic(
            api_key=self.api_key,
            max_retries=0,
            timeout=self.timeout,
        )
        system_message = anthropic.NOT_GIVEN
        if query[0]["role"] == "system":
            system_message = query[0]["content"]
            query = query[1:]
        result = client.messages.create(
            model=self.model,
            messages=query,
            system=system_message,
            temperature=self.temperature,
            **self.kwargs
        )
        return {
            "output": result.content[0].text,
            "input_tokens": result.usage.input_tokens,
            "output_tokens": result.usage.output_tokens,
        }
    
    def google_query(self, query):
        client = genai.Client(api_key=self.api_key, http_options={'api_version':'v1alpha'})
        config = {'thinking_config': {'include_thoughts': True}}
        response = client.models.generate_content(
            model=self.model,
            contents=query,
            config=config,
        )
        return {
            "output": "\n\n".join([response.candidates[0].content.parts[i].text for i in range(len(response.candidates[0].content.parts))]),
            "input_tokens": response.usage_metadata.prompt_token_count,
            "output_tokens": response.usage_metadata.candidates_token_count,
        }
    
    def openai_query(self, query):
        client = OpenAI(api_key=self.api_key, base_url=self.base_url, 
                        timeout=self.timeout, max_retries=0)
        
        response = client.chat.completions.create(
            model=self.model,
            messages=query,
            temperature=self.temperature,
            **self.kwargs
        )

        output = response.choices[0].message.content
        if hasattr(response.choices[0].message, "reasoning_content"):
            output = response.choices[0].message.reasoning_content + "\n\n" + output
        return {
            "output": output,
            "input_tokens": response.usage.prompt_tokens,
            "output_tokens": response.usage.completion_tokens,
        }

    def openai_responses_query(self, query):
        client = OpenAI(api_key=self.api_key, base_url=self.base_url, 
                        timeout=self.timeout, max_retries=0)
        
        response = client.responses.create(
            model=self.model,
            tools=None, # no tools
            store=False, # do not store 
            input=query,
            temperature=self.temperature,
            **self.kwargs
        )

        all_out_msgs = [] 
        for out in response.output:
            if out.type == "message":
                for c in out.content:
                    if c.type == "output_text":
                        all_out_msgs.append({"role": "assistant", "content": c.text})
            elif out.type == "reasoning":
                summary = "<summary>\n"
                for thought in out.summary:
                    if thought.text is not None:
                        summary += "<thought>" + "\n" + thought.text + "\n" + "</thought>\n"
                summary += "</summary>\n"
                all_out_msgs.append({"role": "assistant", "type": "reasoning", "content": summary, "id": out.id})
            else:
                raise ValueError(f"Unknown output type {out.type}.")
        
        if len(all_out_msgs) == 0:
            all_out_msgs.append({"role": "assistant", "content": ""})
    
        return {
            "output": all_out_msgs,
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens,
        }
