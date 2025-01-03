# AutoPAC
Exploring LLMs for Automating Policy to Code Conversion in Business Organizations

# Abstract

Managing systems and network policies for large-scale organizations is challenging for business process automation. Although Policy-as-code (PAC) platforms can ease the task
of policy management by defining and executing systems and network policies in the form of programmable codes, converting existing organizational policies into PAC-compliant code is
not straightforward due to the need for complex dependency resolutions across platforms and applications. On the other hand, policymakers/top management of a business prefer natural
language (NL)-based policies that are easy to comprehend. This paper explores large language models (LLMs) to facilitate the automated conversion of NL-based policies to PAC-complaint code. We observe that public LLMs like ChatGPT need thorough multi-round prompt engineering to generate PAC policies. This concerns privacy and security as the organizational policies are
sensitive business information. Consequently, we explore using a private and personalized setup, like private LLMs. Notably, we observe that existing personalized LLMs like PrivateGPT fail to understand the system-specific policy semantics. Consequently, we develop a framework called AutoPAC, which uses a microservice architecture coupled with fine-tuned models to generate and validate PAC-complaint policies over a personalized LLM framework. An evaluation with more than 100 test cases indicates that the proposed framework effectively generates and validates PAC policies on the fly.

---------------------------------------------------------------------------------------------------

# Directory Structure
```
├── Dataset-AutoPAC          (Contains dataset of policies as codes and annotations that were created, processed and used in AutoPAC)
├── PrivateGPT
├──── Web Engine             (Contains the Python Flask code for Web Engine)
├──── Translator             (Contains the trained LLM and backend tech stack of Translator)
├── Test Setup               (Contains Unit Testing and Judge LLM codes used in AutoPAC)
```
---------------------------------------------------------------------------------------------------

# Setup OPA in Linux Distribution
OPA Setup and Documentation Link: [OPEN POLICY AGENT](https://www.openpolicyagent.org/)

To set up OPA in your system in the terminal:
1. Run `curl -L -o opa https://openpolicyagent.org/downloads/v0.57.0/opa_linux_amd64_static`. The opa file will download in the current directory.
2. Run `sudo chmod 755 ./opa` to set permissions.
3. Export the path to PATH environment variable - `export PATH=$PATH:<path to current opa directory>`.

# Running and Testing Policies in OPA
Running OPA policies against single query:
1. Make input.json file for feeding the query.
2. Run `opa eval -i input.json -d <rego_file> -d <data_file if any> 'data.<package_name_for_rego_file>'`.

Testing OPA policy file with test rego file using unit test framework:
1. Navigate to directory with both rego policy files present.
2. Run `opa test --bundle -v .`
