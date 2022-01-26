from newsletter.settings import TEXT_GEN_PARAMETERS as parameters, API_KEY
import json
import nlpcloud
import datetime

client = nlpcloud.Client("gpt-j", API_KEY, gpu=True)
input_text_template = """This is a list of press release facts, followed by a detailed industry press release based off the facts. The press release is written in the third person with a professional and formal tone.

Press Release Outline:
***
{details}
***

Press Release Title: {title}

Press Release Body:

FOR IMMEDIATE RELEASE

{location}, {release_date} /PRNewswire/ --"""

def format_line(idx, text):
    return str(idx) + ". " + text

def get_pr_prompt(request):
    data = json.loads(request.body.decode('UTF-8'))
    details = data["company_descriptions"] + "\n" + data["pr_details"]

    location = data['location']
    loc_split = location.split(",")
    if len(loc_split) > 1:
        loc_split[0] = loc_split[0].upper()
        location = ','.join(loc_split)
    else:
        location = location.upper()

    submitted_date = datetime.datetime.strptime(data["date"], "%m/%d/%Y")
    date_formatted = submitted_date.strftime("%b %-m, %Y")

    submission_attrs = {
        'title':data["title"],
        'details':details,
        'location':location,
        'release_date':date_formatted
    }

    prompt = input_text_template.format(**submission_attrs)
    print(prompt)

    # reformat for postprocessing
    submission_attrs["release_date"] = submitted_date
    submission_attrs["company_descriptions"] = data["company_descriptions"]
    submission_attrs["details"] = data["pr_details"]
    
    return prompt, submission_attrs

def generate_from_prompt(prompt):
    result = client.generation(str(prompt), top_k=parameters["top_k"], length_no_input=True, max_length=parameters["max_length"], top_p=parameters["top_p"], temperature=parameters["temperature"], repetition_penalty=parameters["repetition_penalty"])
    generated = result["generated_text"]
    start_idx = generated.find("FOR IMMEDIATE RELEASE")
    result["generated_text"] = result["generated_text"][start_idx:]
    result["generated_text"] = result["generated_text"].replace("/PRNewswire/ ", '')
    return result