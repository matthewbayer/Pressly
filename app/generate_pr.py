from newsletter.settings import TEXT_GEN_PARAMETERS as parameters

import json
import nlpcloud

client = nlpcloud.Client("gpt-j", "71764e3a939f49b9ebfbc2e32352bdcfc44b566b", gpu=True)
input_text_template = """This is a list of press release facts, followed by a detailed industry press release based off the facts. The press release includes every fact in the list in order of its appearance.

Press Release Facts:
***
{details}
***

Industry Press Release:

FOR IMMEDIATE RELEASE

BOSTON, Jan. 3, 2022 /PRNewswire/ -- """

def format_line(idx, text):
    return str(idx) + ". " + text

def get_pr_prompt(request):
    data = json.loads(request.body.decode('UTF-8'))
    details = data["company_descriptions"] + data["pr_details"]
    details = [format_line(idx, text) for idx, text in enumerate(details, 1)]

    input_text = "\n".join(details)
    prompt = input_text_template.format(details=input_text)
    print(prompt)
    return prompt

def generate_from_prompt(prompt):
    result = client.generation(str(prompt), top_k=parameters["top_k"], length_no_input=True, max_length=parameters["max_length"], top_p=parameters["top_p"], temperature=parameters["temperature"], repetition_penalty=parameters["repetition_penalty"])
    generated = result["generated_text"]
    start_idx = generated.find("FOR IMMEDIATE RELEASE")
    result["generated_text"] = result["generated_text"][start_idx:] 

    
    return result