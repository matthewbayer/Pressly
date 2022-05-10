from newsletter.settings import TEXT_GEN_PARAMETERS as parameters, API_KEY, GOOSE_API_KEY, DEBUG
from .generation_templates import cow_template
from .models import PressReleaseSubmission
from asgiref.sync import sync_to_async
from django_rq import job

from azureml.exceptions import WebserviceException
from azureml.core.webservice import AksWebservice
from azureml.core import Workspace
from azure.identity import ManagedIdentityCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from azureml.core.authentication import MsiAuthentication

import json
import requests
import time
import asyncio
import os
from datetime import datetime

print("start cred")
credential = ManagedIdentityCredential(managed_identity_client_id="5d738578-badc-4506-805a-8a19c4054644")
msi_auth = MsiAuthentication()
print("start workspace")
ws = Workspace(subscription_id="9d325419-073c-4e8f-a44e-a0479cf3d9ac",
            resource_group="FInalProject",
            workspace_name="5412-gpt2workspace",
            auth=msi_auth)
#connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
print("workspace done")
AZURE_STORAGE_CONNECTION_STRING = 'DefaultEndpointsProtocol=https;AccountName=cs5412meb287;AccountKey=kOm8hJLfPMc+doOA5t+7zHiG9Fi/Zbuw4Lv0syyQVkEhM58uLCTfiOEKzHrfLw+zJba5CfmlTMva+AStOXm4wg==;EndpointSuffix=core.windows.net'
# Create the BlobServiceClient object which will be used to create a container client
blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
print("blob done")
# Create the container
container_client = blob_service_client.get_container_client("eventhub-logs")
print("container done")

try:
    service = AksWebservice(workspace=ws, name='gptjservice')
    print("connected to aks")
except WebserviceException:
    service = None
    print("aks connection failed")


def format_line(idx, text):
    return str(idx) + ". " + text

def get_pr_prompt(request):
    submission_attrs = {
        'iot':get_latest_status()
    }

    prompt = cow_template.format(**submission_attrs)
    #print(prompt)

    # reformat for postprocessing
    return prompt, submission_attrs

def get_latest_status():
    blobs_list = container_client.list_blobs()
    blob_names = []
    for blob in blobs_list:
        blob_names.append(blob.name)
    blob_names = sorted(blob_names, key=lambda x : os.path.basename(x))
    latest = blob_names[-1]
    blob_client = container_client.get_blob_client(latest)
    file_str = blob_client.download_blob().readall().decode("utf-8")
    body_start = file_str.rfind('"Body":') + len('"Body":')
    body = file_str[body_start:-1]
    return body

def generate_from_prompt(prompt):
    #result = client.generation(str(prompt), top_k=parameters["top_k"], length_no_input=True, max_length=parameters["max_length"], top_p=parameters["top_p"], temperature=parameters["temperature"], repetition_penalty=parameters["repetition_penalty"])
    #generated = result["generated_text"]
    if service is None:
        return None
    scoring_uri = service.scoring_uri
    primary, _ = service.get_keys()
    key = primary
    
    input_data = {
        "data":
        [
            {"text":prompt}
        ]
    }
    print(input_data)

    # Set the content type
    headers = {'Content-Type': 'application/json'}
    # If authentication is enabled, set the authorization header
    headers['Authorization'] = f'Bearer {key}'

    print("making request...")
    start = time.time()
    # Make the request and display the response
    resp = requests.post(scoring_uri, json.dumps(input_data), headers=headers)
    print(resp.text)
    res = resp.text
    res = res.replace("\\n", "\n")
    start = res.rfind("Recommendation for cow:")
    res = res[start:]

    newline = res.find("\n")
    if newline != -1:
        res = res[:newline]


    elapsed = time.time() - start
    print(elapsed)
    
    result = {"generated_text": res}
    return result

@job
def generate_press_release(prompt, submission_id, test_delay=1):
    """
    Call external API to generate text for press release. Requires submission_id refers
    to a real PressReleaseSubmission object, else raises ObjectDoesNotExist
    """
    submission = PressReleaseSubmission.objects.get(submission_id=submission_id)
    iot_start = prompt.rfind("Cow status: ")
    iot_end = prompt.rfind("Recommendation for cow:")
    
    submission.iot = prompt[iot_start + len("Cow status: "):iot_end]
    submission.save()
    user = submission.user
    print(DEBUG)
    try:
        if not DEBUG:
            if service is None:
               content = {"generated_text": "Error occurred: Unable to connect to text generation service."}
            else:
                content = generate_from_prompt(prompt)
        else:
            content = {"generated_text": "Test123"}
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
    