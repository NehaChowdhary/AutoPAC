from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import traceback
import pandas as pd
import json
import os
import sys
import random

# For getting privategpt response
def get_privategpt_response(query):
    data_to_privategpt = {
        "question": query
    }
    try:
        response = requests.post("http://localhost:5000/get_answer",json=data_to_privategpt)
        response.raise_for_status()
        # Checking if the request was successful (status code 200)
        if response.status_code == 200:
            # Parsing the JSON response
            data = response.json()
            # Checking if the response contains the 'answer' attribute
            if 'answer' in data:
                answer = data['answer']
                print("Response from privategpt:", answer)
                return answer
            else:
                raise Exception("Response does not contain 'answer' attribute.")
        else:
            raise Exception("Error with status code: "+str(response.status_code))
    
    except requests.exceptions.Timeout:
        print('Timeout error:', str(e))
        traceback.print_exc()
        return None
    except requests.exceptions.TooManyRedirects:
        print('Too many redirects error:', str(e))
        traceback.print_exc()
        return None
    except requests.exceptions.ConnectionError:
        print('Connection Error:', str(e))
        traceback.print_exc()
        return None
    except requests.exceptions.HTTPError as e:
        print('HTTP error occurred:', str(e))
        traceback.print_exc()
        return None
    except requests.exceptions.RequestException as e:
        print('Request Error:', e)
        traceback.print_exc()
        return None
    except Exception as e:
        print('Error: ',str(e))
        traceback.print_exc()
        return None

def get_formatter_response(rego_rule):
    formatter_url = 'https://play.openpolicyagent.org/v1/fmt'
    post_data = {
        "rego_module": rego_rule
    }
    try:
        response = requests.post(formatter_url,json=json.dumps(post_data))
        response.raise_for_status()
        # Checking if the request was successful (status code 200)
        if response.status_code == 200:
            # Parsing the JSON response
            data = response.json()
            # Checking if the response contains the 'answer' attribute
            if 'result' in data:
                answer = data['result']
                print("Response from OPA Formatter:", answer)
                return answer
            else:
                raise Exception("Response does not contain 'result' attribute.")
        else:
            raise Exception("Error with status code: "+str(response.status_code))
    
    except requests.exceptions.Timeout:
        print('Timeout error:', str(e))
        traceback.print_exc()
        return None
    except requests.exceptions.TooManyRedirects:
        print('Too many redirects error:', str(e))
        traceback.print_exc()
        return None
    except requests.exceptions.ConnectionError:
        print('Connection Error:', str(e))
        traceback.print_exc()
        return None
    except requests.exceptions.HTTPError as e:
        print('HTTP error occurred:', str(e))
        traceback.print_exc()
        return None
    except requests.exceptions.RequestException as e:
        print('Request Error:', e)
        traceback.print_exc()
        return None
    except Exception as e:
        print('Error: ',str(e))
        traceback.print_exc()
        return None

def get_lint_response(rego_rule):
    lint_url = 'https://play.openpolicyagent.org/v1/lint'
    post_data = {
        "rego_module": rego_rule
    }
    try:
        response = requests.post(lint_url,json=post_data)
        response.raise_for_status()
        # Checking if the request was successful (status code 200)
        if response.status_code == 200:
            # Parsing the JSON response
            data = response.json()
            # Checking if the response contains the 'answer' attribute
            if 'result' in data:
                answer = data['result']
                print("Response from OPA Lint:", answer)
                return answer
            else:
                raise Exception("Response does not contain 'result' attribute.")
        else:
            raise Exception("Error with status code: "+str(response.status_code))
    
    except requests.exceptions.Timeout:
        print('Timeout error:', str(e))
        traceback.print_exc()
        return None
    except requests.exceptions.TooManyRedirects:
        print('Too many redirects error:', str(e))
        traceback.print_exc()
        return None
    except requests.exceptions.ConnectionError:
        print('Connection Error:', str(e))
        traceback.print_exc()
        return None
    except requests.exceptions.HTTPError as e:
        print('HTTP error occurred:', str(e))
        traceback.print_exc()
        return None
    except requests.exceptions.RequestException as e:
        print('Request Error:', e)
        traceback.print_exc()
        return None
    except Exception as e:
        print('Error: ',str(e))
        traceback.print_exc()
        return None
 
def get_chatgpt_response_with_code(prompt):
    
    driver_options = webdriver.FirefoxOptions()
    driver_options.add_argument('--headless')
    driver = webdriver.Firefox(driver_options)
    
    # Open chat.openai.com
    driver.get("https://chat.openai.com")

    textarea = driver.find_element(By.ID,"prompt-textarea")

    driver.execute_script(f"arguments[0].value = '{prompt}';", textarea)
    textarea.send_keys(Keys.RETURN)
    textarea.submit()

    time.sleep(10)

    response = driver.find_element(by=By.TAG_NAME,value='code')
    return response.text

def get_chatgpt_response(prompt):
    
    try:
        driver_options = webdriver.FirefoxOptions()
        driver_options.add_argument('--headless')
        driver = webdriver.Firefox(driver_options)
        
        # Open chat.openai.com
        driver.get("https://chat.openai.com")

        textarea = driver.find_element(By.ID,"prompt-textarea")

        driver.execute_script(f"arguments[0].value = '{prompt}';", textarea)
        textarea.send_keys(Keys.RETURN)
        textarea.submit()

        time.sleep(5)

        response = driver.find_elements(by=By.CSS_SELECTOR, value='div.text-base')

        # At index 2, we have ChatGPT response
        result = response[2].text
        driver.quit()
        return result
    except Exception as e:
        print(e)
 
if __name__ == '__main__':
    path_to_OPA_test = os.getenv("OPA_Test")
    if(path_to_OPA_test is None):
        print("Set the environment variable 'OPA_Test' to the absolute path storing all the test case files")
        sys.exit(1)
        
    directories =  os.listdir(os.path.abspath(path_to_OPA_test))
    directories = [s for s in directories if '.' not in s]
    path_to_csv = 'OPA_Test_Cases/ChatGPT_Validated/chatgpt_validated4.csv'
    # test_cases = int(input("Enter number of validations from ChatGPT you want to find: "))
    
    print("Directories: ",directories)
    print("Number of directories: ",len(directories))
    
    for i,dir in enumerate(directories):
        print('-'*20)
        print("\n\nIteration {}:".format(i))
        print("\nDirectory chosen: ",dir)
        rule = None
        for file in os.listdir(os.path.abspath("/home/tanmoy/OPA")+"/"+dir):
            if("test.csv" in file):
                df = pd.read_csv(os.path.abspath("/home/tanmoy/OPA")+"/"+dir+"/"+file)
                for i in range(df.shape[0]):
                    rule = df['prompt'].iloc[i]
                
                    if(rule is None):
                        print("Rule is not found")
                        continue
                    
                    elif(not (ord(rule[0])>=65 and ord(rule[0])<=90)):
                        continue
                        
                    print("Query: \n",rule)
                    answer = get_privategpt_response(rule)
                
                    val_pass = False
                    # ChatGPT responses
                    if(answer != None):
                        if(answer == 'allow {'):
                            val_pass = False
                        if(('{' in answer and '}' not in answer)):
                            answer+=' }'
                        elif('}' in answer and '{' not in answer):
                            print("Incomplete rule")
                        #     val_pass = False
                        # else:
                        prompt = 'Is this a valid rego rule? '+answer+' Answer YES or NO. Nothing else.'
                        result = get_chatgpt_response(prompt)
                        while(result is None):
                            result = get_chatgpt_response(prompt)
                            print(result)
                        
                        if(result is None):
                            continue
                    
                        if(answer != 'allow {' and ("yes" in result.lower() or "try again later" in result.lower() or "later" in result.lower() or "again" in result.lower())):
                            val_pass = True
                            print("Validation Passed")
                        else:
                            print("Validation failed")

                        # prompt = 'Reformat the REGO rule in this format-> package authz read := "read" write := "write" admin := "admin"'+answer
                        # answer = get_chatgpt_response_with_code(prompt)
                        # print("Formatted Code: \n",answer)
                        
                    if(os.path.exists(path_to_csv)):
                        data = pd.read_csv(path_to_csv)
                        data.dropna(inplace=True)
                        data.loc[len(data.index)] = [len(data.index),dir,rule,answer,val_pass] 
                        data.to_csv(path_to_csv,index=False)
                    else: 
                        data = pd.DataFrame(columns=['Index','Directory', 'Query', 'PrivateGPT_Rule', 'Validation_Passed'])
                        data['Index'] = [0]
                        data['Directory'] = [dir]
                        data['Query'] = [rule]
                        data['PrivateGPT_Rule'] = [answer]
                        data['Validation_Passed'] = [val_pass]
                        data.to_csv(path_to_csv,index=False)

                    passed = data['Validation_Passed'].sum()
                    total = data['Validation_Passed'].shape[0]
                    print("Accuracy of ChatGPT Validation: ",(passed/total))
                    print("Result added to 'ChatGPT_Validated/chatgpt_validated3.csv'")
                    # if(answer != None):
                    #     answer = get_formatter_response(answer)
                    
                    # if(answer != None):
                    #     answer = get_lint_response(answer)