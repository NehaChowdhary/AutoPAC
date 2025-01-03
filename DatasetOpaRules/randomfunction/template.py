import random
import csv
import string

template = [
    {
        "prompt": "What is Rego?",
        "completion": '''
        Rego is a policy declaration language, which was inspired by Datalog, which is a well understood, decades old query language. Rego extends Datalog to support structured document models such as JSON.
        Rego queries are assertions on data stored in OPA. These queries can be used to define policies that enumerate instances of data that violate the expected state of the system.

        An example of a Rego rule is: 
        [rule_name] if {
                [expression_1],
                [expression_2]
            }
        '''
    },
    {
        "prompt": "Why use Rego?",
        "completion": '''
        Use Rego for defining policy that is easy to read and write.

        Rego focuses on providing powerful support for referencing nested documents and ensuring that queries are correct and unambiguous.

        Rego is declarative so policy authors can focus on what queries should return rather than how queries should be executed. These queries are simpler and more concise than the equivalent in an imperative language.

        Like other applications which support declarative query languages, OPA is able to optimize queries to improve performance.
        '''
    },
    {
        "prompt": "Give an example of Rego rule?",
        "completion": '''
        An example of a Rego rule is: 
        [rule_name] if {
                [expression_1],
                [expression_2]
            }
        '''
    },
    {
        "prompt": "State an example of Rego rule?",
        "completion": '''
        An example of a Rego rule is: 
        [rule_name] if {
                [expression_1],
                [expression_2]
            }
        '''
    },
    {
        "prompt": "Give an example of Rego policy?",
        "completion": '''
        An example of a Rego rule is: 
        [rule_name] if {
                [expression_1],
                [expression_2]
            }
        '''
    },
    {
        "prompt": "State an example of Rego policy?",
        "completion": '''
        An example of a Rego rule is: 
        [rule_name] if {
                [expression_1],
                [expression_2]
            }
        '''
    }
]

expression_choice = ["assignment", "comparison"]
rel_operators = ["<", ">", "==", "<=", ">=", "!="]
dataset = []
rng = 1000
dataset_len = 50000

for _ in range(dataset_len):
    tmp = random.choice(template)
    inputTxt = tmp["prompt"]
    outputTxt = tmp["completion"]

    if ("What" in inputTxt or "example" in inputTxt):

        rule_name_length = random.randint(1, 5)
        rule_name = ''.join(random.choices(string.ascii_lowercase, k=1)) + ''.join(
            random.choices(string.ascii_lowercase + string.digits, k=rule_name_length - 1))
        outputTxt = tmp["completion"].replace("[rule_name]", rule_name)

        for i in range(1, 3):
            exp_choice = random.choice(expression_choice)

            if (expression_choice == "assignment"):

                var_name_length = random.randint(1, 5)
                var_name = ''.join(random.choices(string.ascii_lowercase, k=1)) + ''.join(
                    random.choices(string.ascii_lowercase + string.digits, k=var_name_length - 1))
                value = random.random() * rng

                outputTxt = outputTxt.replace("[expression_" + str(i) + "]", var_name + ":=" + str(value))

            else:
                var_name_length = random.randint(1, 3)
                var_name1 = ''.join(random.choices(string.ascii_lowercase, k=1)) + ''.join(
                    random.choices(string.ascii_lowercase + string.digits, k=var_name_length - 1))
                var_name2 = ''.join(random.choices(string.ascii_lowercase, k=1)) + ''.join(
                    random.choices(string.ascii_lowercase + string.digits, k=var_name_length - 1))

                opr_choice = random.choice(rel_operators)
                outputTxt = outputTxt.replace("[expression_" + str(i) + "]", var_name1 + opr_choice + var_name2)

    dataset.append({"prompt": inputTxt, "completion": outputTxt})

csv_file_name = "kyle-humaneoutput.csv"

with open(csv_file_name, mode='w', newline='') as csv_file:
    fieldnames = ["prompt", "completion"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()

    for test_case in dataset:
        writer.writerow(test_case)

print(f"{len(dataset)} versatile test cases have been written to {csv_file_name}.")