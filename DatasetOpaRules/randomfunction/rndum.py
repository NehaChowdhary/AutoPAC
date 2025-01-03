import random
import csv
import string

template = [
    {
        "prompt": "Give access to Admin to write global config",
        "completion": '''
            allow { 
            object.type == "app_config" 
            subject.global_role == admin 
            action == write 
                }     '''
    },
    {
        "prompt": "Grant Admin access to write teams",
        "completion": '''
        allow { 
                object.type == "team" 
                subject.global_role == admin 
                action == write 
               } '''
    },
    {
        "prompt": "Grant access to Admins to read/write all user sessions",
        "completion": '''
        allow { 
            object.type == "session" 
            subject.global_role == admin 
            action == [read, write][_] 
            } '''
    },
    {
        "prompt": "All users can read labels",
        "completion": '''
        allow { 
        object.type == ""label"" 
        not is_null(subject) 
        action == read 
            }
        '''
    },
    {
        "prompt": "All users can read queries",
        "completion": '''
        allow { 
        not is_null(subject) 
        object.type == ""query"" 
        action == read 
        }'''
    },
    {
        "prompt": "All users can read the global pack",
        "completion": '''
            allow { 
            object.type == ""pack"" 
            not is_null(subject) 
            object.is_global_pack == true 
            action == read 
            }'''
    },
    {
        "prompt": "Allow anyone to list (must be filtered appropriately by the service).",
        "completion": '''
            allow { 
            object.type == ""host"" 
            not is_null(subject) 
            action == list 
            }'''
    },
    {
        "prompt": "Grant read to  global observer",
        "completion": '''
        allow { 
        object.type == ""host"" 
        subject.global_role = observer 
        action == read 
        }'''
    },
    {
        "prompt": " Grant Allow read for matching team admin/maintainer/observer",
        "completion": '''
        allow { 
        object.type == ""host"" 
        team_role(subject, object.team_id) == [admin, maintainer, observer][_] 
        action == read 
        }'''
    },
    {
        "prompt": "Give permission to Allow read/write for global admin/maintainer",
        "completion": '''
        allow { 
        object.type == ""host"" 
        subject.global_role = admin 
        action == [read, write][_] 
        } 
        allow { 
         object.type == ""host"" 
        subject.global_role = maintainer 
        action == [read, write][_] 
        }'''
    },
    {
        "prompt": "Any logged in user can read global config",
        "completion": '''
        allow { 
            object.type == ""app_config"" 
            not is_null(subject) 
            action == read }
            '''
    },
    {
        "prompt": "Any user can read and write self and change their own password.",
        "completion": '''
        allow { 
        object.type == ""user"" 
        object.id == subject.id 
        object.id != 0 
        action == [read, write, change_password][_] 
        }'''
    },
    {
        "prompt": "Any user can read/write own session",
        "completion": '''
        allow { 
        object.type == ""session"" 
        object.user_id == subject.id 
        action == [read, write][_] 
        } '''
    },
    {
        "prompt": "Give permission to Global Admin and Maintainer to read and write policies",
        "completion": '''
        allow { 
        object.type == ""policy"" 
        subject.global_role == [admin,maintainer][_] 
        action == [read, write][_] 
        }

        '''
    },
    {
        "prompt": "Grant permission to Global Observer to read any policies",
        "completion": '''
        allow { 
        object.type == ""policy"" 
        subject.global_role == observer 
        action == read 
        }'''
    },
    {
        "prompt": "Grant permission to Global admins and maintainers to read/write all",
        "completion": '''
         allow { 
        object.type == ""enroll_secret"" 
        subject.global_role == [admin, maintainer][_] 
        action == [read, write][_] 
        } '''
    },
    {
        "prompt": "Grant permission to Global admins and maintainers to read/write all packs",
        "completion": '''
        allow { 
        object.type == ""pack"" 
        subject.global_role == [admin, maintainer][_] 
        action == [read, write][_] 
        } '''
    },
    {
        "prompt": "Give Access to Global admins and maintainers to run any",
        "completion": '''
        allow { 
        object.type == ""targeted_query"" 
        subject.global_role == admin 
        action = run 
            } 
        allow { 
        object.type == ""targeted_query"" 
        subject.global_role == maintainer 
        action = run 
        } 
        allow { 
        object.type == ""query"" 
        subject.global_role == admin 
        action = run_new 
        } 
        allow { 
        object.type == ""query"" 
        subject.global_role == maintainer 
        action = run_new 
        } '''
    },
{
        "prompt": "Give permission to Global admins and maintainers to write queries",
        "completion": '''
        allow { 
        object.type == ""query"" 
        subject.global_role == admin 
        action == write 
        } 
        allow { 
        object.type == ""query"" 
        subject.global_role == maintainer 
        action == write 
        }'''
    },
{
        "prompt": "Give access to Global admins to perform all operations on all users",
        "completion": '''
        allow { 
        object.type == ""user"" 
        subject.global_role == admin 
        action == [read, write, write_role, change_password][_] 
        }'''
    },
{
        "prompt": "Grant permission to Global admins to read/write invites",
        "completion": '''
        allow { 
        object.type == ""invite"" 
        subject.global_role == admin 
        action == [read,write][_] 
        } '''
    },
{
        "prompt": "Grant permission to Global users to read all software",
        "completion": '''
        allow { 
        object.type == ""software_inventory"" 
        subject.global_role == [admin, maintainer, observer][_] 
        action == read 
        } '''
    },
{
        "prompt": "If role is admin or maintainer on any team",
        "completion": '''
        team_role(subject, subject.teams[_].id) == [admin,maintainer][_] 
        action == run_new 
        }'''
    },
{
        "prompt": "Observers can run only if observers_can_run",
        "completion": '''
        allow { 
        object.type == ""targeted_query"" 
        object.observer_can_run == true 
        subject.global_role == observer 
        action = run 
        }'''
    },
{
        "prompt": "Only global admins and maintainers can write labels",
        "completion": '''
        allow { 
        object.type == ""label"" 
        subject.global_role == admin 
        action == write 
        } 
        allow { 
        object.type == ""label"" 
        subject.global_role == maintainer 
        action == write 
        } '''
    },
{
        "prompt": "Give Only permission to global admins to read/write carves",
        "completion": '''
        allow { 
        object.type == ""carve"" 
        subject.global_role == admin 
        action == [read, write][_] 
        }'''
    },
{
        "prompt": "Give Only global users permission to  read activities",
        "completion": '''
        allow { 
        not is_null(subject.global_role) 
        object.type == ""activity"" 
        action == read 
        } '''
    },
{
        "prompt": "Team admin and maintainer can run a new query",
        "completion": '''
        allow { 
        object.type == ""query"""
        Team admin and maintainers can read and write policies for their teams,"allow { 
        not is_null(object.team_id) 
        object.type == ""policy"" 
        team_role(subject, object.team_id) == [admin,maintainer][_] 
        action == [read, write][_] 
        }'''
    },
{
        "prompt": "Team admin can write teams",
        "completion": '''
        allow { 
        object.type == ""team"" 
        team_role(subject, object.id) == admin 
        action == write 
        }'''
    },
{
        "prompt": "Team admin, maintainers and observers can read global policies",
        "completion": '''
        allow { 
        is_null(object.team_id) 
        object.type == ""policy"" 
        team_role(subject, subject.teams[_].id) == [admin,maintainer,observer][_] 
        action == read 
        }'''
    },
{
        "prompt": "Team admins and maintainers can create assignment of  new queries",
        "completion": '''
        allow { 
        object.id == 0 # new queries have ID zero 
        object.type == ""query"" 
        team_role(subject, subject.teams[_].id) == [admin, maintainer][_] 
        action == write 
        }'''
    },
{
        "prompt": "Team admins and maintainers can edit and delete only their own queries",
        "completion": '''
        allow { 
        object.author_id == subject.id 
        object.type == ""query"" 
        team_role(subject, subject.teams[_].id) == [admin,maintainer][_] 
        action == write 
        }'''
    },
{
        "prompt": "Team admins and maintainers can read/write for appropriate teams",
        "completion": '''
        allow { 
        object.type == ""enroll_secret"" 
        team_role(subject, object.team_id) == [admin, maintainer][_] 
        action == [read, write][_] 
        }'''
    },
{
        "prompt": "Team users can read all software in their teams",
        "completion": '''
        allow { 
        not is_null(object.team_id) 
        object.type == ""software_inventory"" 
        team_role(subject, object.team_id) == [admin, maintainer, observer][_] 
        action == read 
        }'''
    },
{
        "prompt": "filtered to only teams that they maintain",
        "completion": '''
        allow { 
        object.type == ""targeted_query"" 
        object.observer_can_run == false 
        is_null(subject.global_role) 
        action == run not is_null(object.host_targets.teams)  
        ok_teams := { tmid | tmid := object.host_targets.teams[_]; team_role(subject, tmid) == [admin,maintainer][_] } 
        count(ok_teams) == count(object.host_targets.teams) 
        }'''
    },
{
    "prompt": "if the user has no explicit role for that team",
    "completion": '''
         team_role(subject, team_id) = role { 
        subject_team := subject.teams[_] 
        subject_team.id == team_id 
        role := subject_team.role 
        } '''
    },
{
    "prompt": "global admins or global maintainers",
    "completion": '''
    allow { 
            object.type == ""team"" 
            object.id != 0 
            subject.global_role == [admin, maintainer][_] 
            action == read 
           } 
          '''
    },
{
    "prompt": " give assignment target teams",
    "completion": '''
         allow { 
            object.type == ""targeted_query"" 
            object.observer_can_run == true 
            is_null(subject.global_role) 
            action == run '''
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

    if ("Grant" in inputTxt or "access" in inputTxt):

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

csv_file_name = input("Enter output CSV file name: ")

with open(csv_file_name, mode='w', newline='') as csv_file:
    fieldnames = ["prompt", "completion"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()

    for test_case in dataset:
        writer.writerow(test_case)

print(f"{len(dataset)} versatile test cases have been written to {csv_file_name}.")
