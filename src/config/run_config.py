from enum import Enum
from typing import Any, List, Optional, Tuple, Union

from pydantic import Field, validator

from config.utils import PydanticBaseModelWithOptionalDefaultsPath as PBMwODP

class SolverEnum(str, Enum):
    CoT = "CoT"
    code = "code"

class InferenceConfig(PBMwODP, extra="forbid"):  # type: ignore
    temperature: float = Field(..., description="Temperature for sampling")
    top_p: float = Field(..., description="Top p for sampling")
    max_tokens: Optional[int] = Field(..., description="Max tokens for sampling")
    concurrent_requests: int = Field(..., description="API concurrent requests")
    timeout: int = Field(500, description="Timeout for API")

class SolverConfig(PBMwODP, extra="forbid"):  # type: ignore
    type_solver: SolverEnum = Field(SolverEnum.CoT, description="Type of solver")
    system_prompt: str = Field(None, description="System prompt for the model")
    parse_feedback: bool = Field(False, description="Parse feedback")
    check_feedback: bool = Field(False, description="Parse feedback")
    max_feedback_rounds: int = Field(1, description="Max feedback rounds")
    formatting_prefix: str = Field("Format your reply as follows:", description="Formatting prefix for the model")
    error_string: str = Field(None, description="Error string for the model")
    give_solution: bool = Field(False, description="Give solution to the model")
    batch_size: int = Field(10, description="Batch size for processing")

    # code specific
    image_name: str = Field("mathconstruct-sandbox", description="Docker image name")
    timeout: float = Field(10, description="Timeout for code execution in seconds")
    cpus: int = Field(1, description="Number of cpus used in each code execution")
    memory: int = Field(1, description="Memory in GB used in each code execution")
    n_parallel_code_executions: int = Field(2, description="Number of parallel code executions")
    max_code_iterations: int = Field(2, description="Max code iterations for code execution in model answer")
    code_feedback_prompt: str = Field("Code Output:\n```{feedback}```\n", description="Code feedback prompt")
    stop_at_timeout: bool = Field(False, description="Stops the LLM after timeout has occurred (brute force).")
    last_code_iteration_warning: str = Field("This was the last time your code can be executed. From now on, you will not be able to execute code.", description="Last code iteration warning")

class RunConfig(PBMwODP):
    test_run: bool = Field(False, description="Test run: don't save results, run parse+check, print to stdout")
    output_dir: str = Field(None, description="Output directory under outputs/, defaults to timestamp")
    input_dir_revisions: str = Field(None, description="Input directory of revision problems if running on revisions")
    models: List[str] = Field(..., description="List of api:model_name pairs")
    inference: InferenceConfig
    solver: SolverConfig
    problems: List[str] = Field(..., description="List of problem regexes, we run the union of all matched problems")
    n_variations: int = Field(..., description="Number of variations to generate for each problem")
    tags: List[str] = Field([], description="List of problem tags to filter by.")
    n_try_variations: Optional[int] = Field(None, description="Number of variations to generate for each problem before filtering by tags")