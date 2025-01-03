import requests
import json
import pandas as pd
import re

# API endpoint URLs
FORMATTER_URL = 'https://play.openpolicyagent.org/v1/fmt'
LINT_URL = 'https://play.openpolicyagent.org/v1/lint'
PRIVATEGPT_URL = 'http://localhost:5000/get_answer'

PRIVATEGPT_HEADERS = {"Content-Type": "application/json"}

sentence = 'package abc'

# Data to be sent in the POST request
POST_DATA = {
    "rego_module": sentence
}

# Process OPA format function
def process_fmt(post_data):
    try:
        response = requests.post(FORMATTER_URL, json=post_data)

        if('result' not in response.json()):
            raise requests.RequestException("Result not present in fmt response")
        print(response.json()["result"])

        if response.status_code // 100 == 2:
            print("Formatting successful. Processing lint")
        else:
            print(f'Error making POST request. Status code: {response.status_code}')
            
        return response

    except requests.RequestException as e:
        print('Error:', e)

def process_lint(post_data):
    try:
        response = requests.post(LINT_URL, json=post_data)

        if (response.status_code // 100) != 2:
            print(f'Error making POST request. Status code: {response.status_code}')

        return response
    
    except requests.RequestException as e:
        print('Error:', e)

def process_privategpt(post_data):
    try:
        privategpt_req_body = {"query": post_data}
        privategpt_req_body = json.dumps(privategpt_req_body)
        privategpt_response = requests.post(PRIVATEGPT_URL,json=privategpt_req_body,headers=PRIVATEGPT_HEADERS)
        
        if (privategpt_response.status_code // 100) != 2:
            print(f'Error making POST request. Status code: {privategpt_response.status_code}')

        return privategpt_response
        
    except requests.RequestException as e:
        print('Error:', e)

if __name__ == '__main__':
    
    try:
        
        # Include data fetch code from privategpt server
        queries_df = pd.read_csv("queries.csv")
        query = queries_df.sample(n=1)
        query_placeholder = query["prompt"].iloc[0]
        
        print("Query asked: ",query_placeholder)
        
        response_privategpt = process_privategpt(query_placeholder)
        if (response_privategpt.status_code // 100) != 2:
            raise requests.RequestException('Error from PrivateGPT Server Endpoint! Status Code: {}'.format(response_privategpt.status_code))
        
        print("PrivateGPT response raw: ",response_privategpt)
        response_privategpt = response_privategpt.json()
        print("PrivateGPT response: ",response_privategpt)
        
        privategpt_answer = response_privategpt["answer"]
        
        print("PrivateGPT Answer: {}".format(privategpt_answer))
        
        if(privategpt_answer == ""):
            raise requests.RequestException('PrivateGPT Response Empty!')
        
        delimiters = r'.'
        privategpt_answer_sentences = re.split(delimiters,privategpt_answer)
        
        for privategpt_answer in privategpt_answer_sentences:
            POST_DATA["rego_module"] = privategpt_answer
            
            if(privategpt_answer is None):
                continue
            
            print("PrivateGPT Answer: {}".format(privategpt_answer))
            
            response_fmt = process_fmt(post_data=POST_DATA)
            while(response_fmt is None):
                print("Re-sending fmt request!")
                response_fmt = process_fmt(post_data=POST_DATA)
            if((response_fmt.status_code // 100) != 2):
                raise requests.RequestException('Error from FMT Endpoint! Status Code: {}'.format(response_fmt.status_code))

            response_fmt = response_fmt.json()
            print(response_fmt)
            POST_DATA["rego_module"] = response_fmt["result"]
            response_lint = process_lint(post_data=POST_DATA)

            while(response_lint is None):
                print("Re-sending lint request!")
                response_fmt = process_lint(post_data=POST_DATA)
            if((response_lint.status_code // 100) != 2): 
                raise requests.RequestException('Error from LINT Endpoint! Status Code: {}'.format(response_fmt.status_code))

            print(response_lint.json())
        
    except requests.RequestException as e:
        print('Error: ',e)
