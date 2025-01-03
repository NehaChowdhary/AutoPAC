import pandas as pd
import os
import random
import sys
import traceback
import requests
import time

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


if __name__ == '__main__':
    df = pd.DataFrame(columns=['Index','Directory','Query','PrivateGPT_Rule','Time_Required'])
    # print(df.shape[0])
    path_to_OPA_test = os.getenv("OPA_Test")
    if(path_to_OPA_test is None):
        print("Set the environment variable 'OPA_Test' to the absolute path storing all the test case files")
        sys.exit(1)
        
    directories =  os.listdir(os.path.abspath(path_to_OPA_test))
    directories = [s for s in directories if '.' not in s]
    
    test_cases = int(input("Enter number of validations from ChatGPT you want to find: "))
    
    for i in range(test_cases):
        print('-'*20)
        print("\n\nIteration {}:".format(i))
        dir = random.choice(directories)
        print("\nDirectory chosen: ",dir)
        rule = None
        for file in os.listdir(os.path.abspath("/home/tanmoy/OPA")+"/"+dir):
            if("test.csv" in file):
                df_rules = pd.read_csv(os.path.abspath("/home/tanmoy/OPA")+"/"+dir+"/"+file)
                rule = df_rules.sample(n=1)['prompt'].iloc[0]
                
        if(rule is None):
            print("Rule is not found")
            continue
        elif(not (ord(rule[0])>=65 and ord(rule[0])<=90)):
            continue
        
        print("Query: \n",rule)
        time_start = time.time()
        answer = get_privategpt_response(rule)
        time_end = time.time()
        time_required = time_end - time_start
        # print(df.shape[0])
        if(df.shape[0] == 0):
            df['Index'] = [0]
            df['Directory'] = [dir]
            df['Query'] = [rule]
            df['PrivateGPT_Rule'] = [answer]
            df['Time_Required'] = [time_required]
        else:
            # print(df.head())
            df.loc[len(df.index)] = {'Index': len(df.index),'Directory': dir,'Query': rule,'PrivateGPT_Rule': answer,'Time_Required': time_required}
        
df.to_csv('Time_Metric.csv',index=False)
print("Entries added to Time_Metric.csv")
        