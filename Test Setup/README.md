# Testing of PrivateGPT Model

Each response of the PrivateGPT model for a particular policy has to be tested rigorously. For this purpose, we need to -
1. Provide a query to the model (fetched randomly from **queries.csv**).
2. Record its response. Split it into explanation and code parts.
3. Format the code portion properly with OPA fmt API and check for lint violations from OPA lint API.
4. Create a file with the REGO code and test it from OPA unit testing framework.

The **lint_opa.py** does all these together, **Lint_Opa.ipynb** simply offers an interactive notebook environment for the same.

# Testing ChatGPT judge setup

1. Install Firefox webdriver [geckodriver](https://github.com/mozilla/geckodriver/releases) and add it to PATH variable of your system.
2. Install selenium if not already installed with `pip install selenium`.
3. Assign environment variable OPA_Test=<absolute_path_to_OPA_TestCases_Directory>
4. Run `python OpenAI_Judge.py`. Wait for 20 seconds to receive generated output. Additionally, it will be appended to 'OPA_Test_Cases/ChatGPT_Validated/chatgpt_validated2.csv'.

# Testing framework execute

Follow these instructions to execute the testing framework - 
1. Run `python lint_opa.py`.
2. Wait for each part as explained above.

**Note:** PrivateGPT server should be listening to 5000 port. Follow the SETUP.md instructions in privateGPT directory for it.

**PrivateGPT Logger Files**

The privategpt_logger.sh file creates a file structure logging the resources used by PrivateGPT (CPU and Memory).

# OPA Test Cases
Each of the directories have OPA unit test cases pertaining to a particular use-case. 

For running OPA test cases, OPA has to be installed - 
1. Download the opa v0.63 executable - `curl -L -o opa https://openpolicyagent.org/downloads/v0.63.0/opa_linux_amd64_static`.
2. Make it executable - `chmod 755 ./opa`.
3. Alias the executable with - `alias opa='<path_where_opa_installed>/opa'`.
4. Navigate to the respective test directory in the OPA_Test_Cases and run `opa test -v .`.
