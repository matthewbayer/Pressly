from newsletter.settings import TEXT_GEN_PARAMETERS as parameters, API_KEY, DEBUG
from .generation_templates import press_release_template
from .models import PressReleaseSubmission
from asgiref.sync import sync_to_async
from django_rq import job

import json
import nlpcloud
import openai
from datetime import datetime
import requests
import time
import asyncio

#client = nlpcloud.Client("gpt-j", API_KEY, gpu=True)


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

    try:
        submitted_date = datetime.strptime(data["date"], "%m/%d/%Y")
    except ValueError: # Fallback to today's date
        submitted_date = datetime.now()
    
    date_formatted = submitted_date.strftime("%b %-m, %Y")

    submission_attrs = {
        'title':data["title"],
        'details':details,
        'location':location,
        'release_date':date_formatted
    }

    prompt = press_release_template.format(**submission_attrs)
    #print(prompt)

    # reformat for postprocessing
    submission_attrs["release_date"] = submitted_date
    submission_attrs["company_descriptions"] = data["company_descriptions"]
    submission_attrs["details"] = data["pr_details"]
    
    return prompt, submission_attrs

def generate_from_prompt(prompt):
    #result = client.generation(str(prompt), top_k=parameters["top_k"], length_no_input=True, max_length=parameters["max_length"], top_p=parameters["top_p"], temperature=parameters["temperature"], repetition_penalty=parameters["repetition_penalty"])
    #generated = result["generated_text"]
    completion = openai.Completion.create(
        engine="gpt-neo-20b",
        prompt=prompt,
        max_tokens=500,
        temperature=1.2,
        top_k=20,
        top_p=0.7,
        stream=False)
    all_text = prompt + completion['choices'][0]['text']
    result = {"generated_text": all_text}
    start_idx = all_text.find("FOR IMMEDIATE RELEASE")
    result["generated_text"] = result["generated_text"][start_idx:]
    result["generated_text"] = result["generated_text"].replace("/PRNewswire/ ", '')
    return result

@job
def generate_press_release(prompt, submission_id, test_delay=6):
    """
    Call external API to generate text for press release. Requires submission_id refers
    to a real PressReleaseSubmission object, else raises ObjectDoesNotExist
    """
    submission = PressReleaseSubmission.objects.get(submission_id=submission_id)
    user = submission.user
    print("begin")
    try:
        if not DEBUG:
            content = generate_from_prompt(prompt)
        else:
            content = {"generated_text": "test content\n\testing\nasdasfas\n\nabc123"}
            time.sleep(test_delay)
        content["generated_text"] = content["generated_text"].replace("\n", "\n")
        submission.generated_text = content["generated_text"]
        submission.set_complete()
        print("Done")
        user.num_credits = user.num_credits - 1
        user.save()

    except requests.exceptions.RequestException as e:
        submission.error_msg = "An error occurred generating your content. Please try again."
        submission.set_error()
        print(e)
    except ValueError:
        submission.error_msg = "Error reading in your submission - ensure your date is properly formatted."
        submission.set_error()
    