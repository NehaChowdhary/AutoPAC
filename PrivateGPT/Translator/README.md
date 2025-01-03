# Setup PrivateGPT server

1. Concatenate the split_model files into one file -
   
            mkdir codet5_fine_tuned
            cat codet5_fine_tuned_split/* > codet5_fine_tuned/codet5-fine-tuned.ckpt
2. Run `pip install -r requirements.txt` to install dependencies.
3. Run  `python privateGPT_server.py` to start the server at port 5000.

[Note: Follow instructions in privategpt_client directory to start the frontend React development server for the client app.]



# Setup Conda Environment

1. Download miniconda using:
   `mkdir -p ~/miniconda3`
   `wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh`
   `bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3`
   `rm -rf ~/miniconda3/miniconda.sh`

2. Deactivate base env using:
   `conda deactivate`
   
4. Activate the llm-train env using in policy_GPT/privateGPT_new/privategpt_server:
   `conda env create -f environment.yaml`

5. Start the llm-train environment using:
   `conda activate llm-train`

6. Create the required environment variables using:
   `export MODEL_DIR=<Path_till_codet5-fine-tuned.ckpt>`
   `export MODEL_NAME=Salesforce/codet5-small`
   
7. To check in Thunderclient (only Server):
   POST request
   http://localhost:5000/get_answer
   {
     "question": "Implement a REGO rule tm09m if dr==aw, d<=c and ixm>x6k."
   }
