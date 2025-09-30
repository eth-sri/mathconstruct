import json
import os
import re
import argparse 
from fasthtml.common import *
from math_construct.problems import get_problem_class
from scripts.analyze import analyze_run
from math_construct.problems import get_all_problem_classes
import yaml 
from loguru import logger

"""
    A dashboard app that shows all about a run 
"""

parser = argparse.ArgumentParser()
parser.add_argument("--run", type=str, required=True) # 'logs/example-run'
parser.add_argument("--models", type=str, nargs="+", default=None)
parser.add_argument("--problems", type=str, nargs="+", default=None)
parser.add_argument("--max_variations", type=int, default=4)
args = parser.parse_args()

# Analyze run 
run_dir = args.run
#logger.info(f"Analyzing run {run_dir}.")
#results = analyze_run(run_dir, args.models, args.problems, max_variations=args.max_variations)[0]
results = {} 
#logger.info(f"Done analyzing run {run_dir}.")

# Prepare problem classes
problem_classes = get_all_problem_classes()
problem_classes = {problem_class.config.name: problem_class for problem_class in problem_classes}

app, rt = fast_app(live=False, hdrs=[
    Meta(name="color-scheme", content="only light"),
    #KatexMarkdownJS(),
    Style("""
    .sidebar {
        display: inline-block;
        width: 30%;
        min-width: 30%;
        height: 100%;
        overflow-y: auto;
        background-color: #f8f9fa;
        padding: 20px;
        border-right: 1px solid #dee2e6;
        padding-right: 20px;
        z-index: 100;
    }
    .sidebar-list {
        max-height: 1000px;
        position: relative;
        overflow-y: scroll;
    }
    .sidebar-item {
        display: block;
        padding: 8px;
        color: #333;
        text-decoration: none;
        border-radius: 4px;
    }
    .reload-button {
        font-style: italic;
        color: #002f94;
    }
    .sidebar-item.current {
        background-color: #e9ecef;
    }
    .sidebar-item:hover {
        background-color: #e9ecef;
    }
    .main {
        display: inline-block;
        width: 70%;
        overflow-x: auto;
        height: 100%;
        margin: 0% 2%;
    }
    .strong {
        font-weight: bold;
    }
    .fake-hr {
        border-bottom: 5px solid #333;
        margin: 1rem 0;
    }
    .problem-stats {
        white-space:pre;
        font-family:monospace;
    }
    .box {
        width: 100%;
        margin: 0rem 0rem 1.5rem 0rem;
        padding: 2rem 2rem 1.5rem 2rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        max-height: 500px;
        position: relative;
        overflow-y: scroll;
    }
    .problem-box {
        background-color: #c7d9ff;
    }
    .solution-box {
        background-color: #ffd700;
        border: 2px solid;
    }
    .response-box {
        background-color: #ffe4c8;
        font-weight: normal;
    }
    .response-box-details {
        padding: 0rem 0rem;
    }
    .answer-box {
    }
    .details-box {
        
    }
    .correct {
        background-color: #c7ffcb;
    }
    .incorrect {
        background-color: #ffcbc7;
    }
    details > summary {
        list-style-type: '▶️ ';
    }
    details[open] > summary {
        list-style-type: '🔽 ';
    }
    details summary::after {
        display: none;
    }
    .user {
        background-color: #d1bca5;
    }
    .assistant {
        background-color: #ffe4c8;
    }
""")])

title = f"Run Analysis: {run_dir}"

def get_problem_stats(results, model, problem):
    res = results[model][problem] 
    corrects = [inst['is_correct'] for inst in res]
    if len(corrects) == 0:
        return {
            "nb_instances": 0,
            "corrects": [],
            "accuracy": 0,
        }
    nb_inst = len(corrects)
    acc = sum(corrects) / nb_inst 
    return {
        "nb_instances": nb_inst,
        "corrects": corrects,
        "accuracy": acc,
    }

def get_problem_ticks(results, model, problem):
    stat = get_problem_stats(results, model, problem)
    ticks = ""
    for i, correct in enumerate(stat['corrects']):
        ticks += f"{'✅' if correct else '❌'}"
    return ticks

def get_model_stats(results, model):
    res = results[model] 
    nb_problems = len(res)
    problem_stats = {problem: get_problem_stats(results, model, problem) for problem in res.keys()}
    stats = {'problem_stats': problem_stats.copy()}
    stats['nb_problems'] = len(res)
    stats['avg_accuracy'] = sum([stat['accuracy'] for stat in problem_stats.values()]) / nb_problems
    return stats 

def model_stats_to_html(stats):
    problem_stats_html = [] 
    for problem, stat in stats['problem_stats'].items():
        p = f"{problem}:{' '*(30-len(problem))}"
        p += f"{stat['accuracy']*100:.2f}% " 
        p += f"({stat['nb_instances']} instances: "
        for i, correct in enumerate(stat['corrects']):
            p += f"{'✅' if correct else '❌'}"
        p += ")"
        logger.info(p)
        problem_stats_html.append(P(p, cls="problem-stats"))
    stats_html = [
        P(f"Avg Acc: {stats['avg_accuracy']*100:.2f}% ({stats['nb_problems']} problems)", cls="strong"),
        Div(*problem_stats_html)
    ]
    return stats_html

def parse_messages_response(response):
    # This is a list of messages
    response_str = response[0]["content"]
    for i in range(1, len(response)):
        if response[i]["role"] == "assistant":
            response_str += "\n\n" + 30 * "=" + "Assistant" + 30 * "=" + "\n\n" + response[i]["content"]
        else:
            response_str += "\n\n" + 30 * "=" + "User" + 30 * "=" + "\n\n" + response[i]["content"]
    return response_str

def sanitize_response(response):
    response = response.replace("\\( ", "$")
    response = response.replace(" \\)", "$")
    response = response.replace("\\(", "$")
    response = response.replace("\\)", "$")

    response = response.replace("\\[ ", "$$")
    response = response.replace(" \\]", "$$")
    response = response.replace("\\[", "$$")
    response = response.replace("\\]", "$$")
    return response

###### results

@rt("/refresh/{url}")
def get(url: str):
    global results
    results = analyze_run(run_dir, args.models, args.problems, max_variations=args.max_variations)[0]
    logger.info("Refreshed!")
    if url == "" or url is None:
        return Redirect("/")
    url = '/view/' + url.replace('>>>', '/')
    return Redirect(url)

@rt("")
def index():
    # add button that calls /refresh 
    links = [
        A("[Reload All Data]", href="/refresh/", cls="sidebar-item reload-button strong"), 
        A("Home", href="/", cls="sidebar-item strong")
    ] 
    for model in results.keys():
        links.append(A(model, href=f"/view/{model}", cls="sidebar-item"))

    stats_html = [] 
    for model in results.keys():
        stats = get_model_stats(results, model)
        stats_html.append(H3(f"Model: {model}"))
        stats_html.append(Div(*model_stats_to_html(stats)))
    
    return Titled(title, Div(
        Div(*links, cls="sidebar"),
        Div(
            Div(*stats_html),
            cls="main"
        ),
        style="display: flex; width: 100%"
    ))

@rt("/view/{model}")
def get(model: str):
    logger.info("model: ", model)
    links = [
        A("[Reload All Data]", href=f"/refresh/{model}", cls="sidebar-item reload-button strong"), 
        A("Home", href="/", cls="sidebar-item strong")
    ] 
    links.append(A(f"  {model}", href=f"/view/{model}", cls="sidebar-item strong current"))

    for problem in results[model].keys():
        ticks = get_problem_ticks(results, model, problem)
        link_text = f"{problem} {ticks}"
        links.append(A(link_text, href=f"/view/{model}/{problem}", cls="sidebar-item"))
    
    stats = get_model_stats(results, model)
    stats_html = Div(*model_stats_to_html(stats))

    d = Div(*links[3:], cls="sidebar-list")
    sidebar = Div(*links[:3], d, cls="sidebar")
    return Titled(title, Div(
        sidebar,
        Div(
            H3(f"Model: {model}", style="text-align: left;"),
            Div(stats_html),
            cls="main"
        ),
        style="display: flex; width: 100%"
    ))

@rt("/modelinteraction/{id}")
def get(id: str): #model>>problemname>>id
    model, problem_name, i = id.split(">>")
    entry = results[model][problem_name][int(i)]

    if type(entry["response"]) == list and not isinstance(entry["response"][0], dict):
        response = "\n\n".join(entry["response"])
        response = sanitize_response(response)
        response_box = Div(response, cls="marked box response-box")
        return response_box
    else:
        responses = entry["response"]
        response_boxes = []
        for response in responses:
            role, content, type_ = response["role"], response["content"], response.get("type", "")
            response = sanitize_response(content)
            response_boxes.append(P(f"Role: {role}", cls="strong"))

            if role == 'code' or role == "tool" or type_ == "code_interpreter_call":
                # try to parse it as a dict
                try:
                    response_dict = json.loads(response)
                    if "tool_name" in response_dict and response_dict["tool_name"] == "execute_code":
                        code = response_dict["tool_arguments"]["code"]
                    else:
                        code = response
                except:
                    code = response
                response = code.replace('```python','').replace('```', '').strip()
                response = Pre(Code(code), cls=f"language-python marked box response-box code")
            else:
                response = Div(response, cls=f"marked box response-box {role}")
            response_boxes.append(response)
        return Div(*response_boxes)

@rt("/view/{model}/{problem_name}")
def get(model: str, problem_name: str):
    logger.info("model: ", model, "problem_name: ", problem_name)
    links = [
        A("[Reload All Data]", href=f"/refresh/{model}>>>{problem_name}", cls="sidebar-item reload-button strong"), 
        A("Home", href="/", cls="sidebar-item strong")
    ] 
    links.append(A(f"  {model}", href=f"/view/{model}", cls="sidebar-item strong"))

    for problem in results[model].keys():
        ticks = get_problem_ticks(results, model, problem)
        cls = "sidebar-item" if problem != problem_name else "sidebar-item current"
        link_text = f"{problem} {ticks}"
        links.append(A(link_text, href=f"/view/{model}/{problem}", cls=cls))
    ticks = get_problem_ticks(results, model, problem_name) # my ticks

    res = results[model][problem_name]
    instances_html = []
    for i, entry in enumerate(res): 
        try:
            problem_class = problem_classes[problem_name]
            instance = problem_class.from_json(entry["problem"])
        except Exception as e:
            logger.info(f"Error parsing an instance of the problem {problem_name}: {e}")
            continue
        answer, is_correct = entry["answer"], entry["is_correct"]
        verdict = "✅" if is_correct else "❌"
        correct_cls = "correct" if is_correct else "incorrect"
        parsecheck_details = entry["parsecheck_details"]

        curr_html = [Div(cls=f"fake-hr")]
        orig_suffix = f" (Original)" if instance.is_original() else ""
        curr_html.append(H3(f"Problem Instance #{i}{orig_suffix}:", cls="strong problem-instance-p"))
        curr_html.append(Div(str(instance), cls="marked box problem-box"))

        formatting_instructions = instance.get_formatting()
        curr_html.append(P(f"Formatting Instructions:", cls="strong"))
        curr_html.append(Div(formatting_instructions, cls="marked box problem-box"))

        solution = instance.get_solution()
        if solution is not None:
            curr_html.append(P(f"Our Solution:", cls="strong"))
            curr_html.append(Div(solution, cls="marked box solution-box"))

        # Lazy population 
        extras = {'id': f"{model}>>{problem_name}>>{i}"}
        curr_html.append(Details(Summary("Model Interaction:"), cls="response-box-details strong", **extras))
        
        curr_html.append(P(f"Parsed Answer ({verdict}):", cls="strong"))
        curr_html.append(Div(answer, cls=f"box answer-box {correct_cls}"))
        if not is_correct:
            curr_html.append(P(f"Parsecheck Details:", cls="strong"))
            curr_html.append(Div(parsecheck_details, cls=f"box details-box {correct_cls}"))

        instances_html.append(Div(*curr_html))
    
    # Add script to scroll to current item
    mathjaxsetup=Script("""
        window.MathJax = {
        tex: {
            inlineMath: [['$', '$']]
        }
        };
    """)
    mathjax=Script(id="MathJax-script", src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js")
    scroll_and_lazyfetch_script = Script("""        
        document.addEventListener('DOMContentLoaded', function() {
            const current = document.querySelector('.sidebar-item.current');
            if (current) {
                current.scrollIntoView({ behavior: 'auto', block: 'center' });
            }
        });

        document.addEventListener('DOMContentLoaded', function() {
            document.querySelectorAll('.response-box-details').forEach(function(element) {
                element.addEventListener('toggle', function(event) {
                    if (event.target.open) { // Check if the <details> is being opened
                        const idd = event.target.getAttribute('id');
                        if (!event.target.hasAttribute('data-loaded')) {
                            fetch(`/modelinteraction/${idd}`)  // Assuming you have a backend route to handle this
                                .then(response => response.text())
                                .then(data => {
                                    event.target.innerHTML += data; // Append or replace this with actual structure
                                    event.target.setAttribute('data-loaded', true); // Mark as loaded
                                    MathJax.typesetPromise();
                                })
                                .catch(error => console.error('Error fetching response details:', error));
                        }
                    }
                });
            });
        });
    """)

    d = Div(*links[3:], cls="sidebar-list")
    sidebar = Div(*links[:3], d, cls="sidebar")
    return Titled(title, Div(
        mathjaxsetup,
        mathjax,
        sidebar,
        scroll_and_lazyfetch_script,
        Div(
            H3(f"Model: {model}", style="text-align: left;"),
            H3(f"Problem: {problem_name} {ticks}", style="text-align: left;"),
            *instances_html,
            cls="main"
        ),
        style="display: flex; width: 100%"
    ))

###
serve(reload=False)
