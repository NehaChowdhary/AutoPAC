from transformers import AutoTokenizer, T5ForConditionalGeneration  
from transformers import AdamW
from t5model import T5Model
import torch
import pytorch_lightning as pl
from pytorch_lightning.callbacks import ModelCheckpoint
from torch.nn.utils.rnn import pad_sequence
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import warnings
from waitress import serve

pl.seed_everything(100)
warnings.filterwarnings("ignore")

# Define Macros and Constants
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
INPUT_MAX_LEN = 128 #input length
OUTPUT_MAX_LEN = 128 # output length
TRAIN_BATCH_SIZE = 8 # batch size of training
VAL_BATCH_SIZE = 2 # batch size for validation
EPOCHS = 5 # number of epoch    
MODEL_NAME = os.environ.get("MODEL_NAME")
MODEL_DIR = os.environ.get("MODEL_DIR")

# Fetch the model from its checkpoint
print(MODEL_DIR)
train_model = T5Model.load_from_checkpoint(MODEL_DIR)
train_model.freeze()    # Freeze the layers of the model

# Fetch tokenizer
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

# generate question controller function
def generate_question(question):

    inputs_encoding =  tokenizer(
        question,
        add_special_tokens=True,
        max_length= INPUT_MAX_LEN,
        padding = 'max_length',
        truncation='only_first',
        return_attention_mask=True,
        return_tensors="pt"
        )

    
    generate_ids = train_model.model.generate(
        input_ids = inputs_encoding["input_ids"],
        attention_mask = inputs_encoding["attention_mask"],
        max_length = INPUT_MAX_LEN,
        num_beams = 4,
        num_return_sequences = 1,
        no_repeat_ngram_size=2,
        early_stopping=False,
        )

    preds = [
        tokenizer.decode(gen_id,
        skip_special_tokens=True, 
        clean_up_tokenization_spaces=True)
        for gen_id in generate_ids
    ]
    return "".join(preds)

def create_privategpt_server():
    app = Flask(__name__) #creating the Flask class object   
    CORS(app) 
    
    @app.route('/get_answer',methods=['POST']) # Controller method for /get_answer endpoint   
    def get_answer():  
        json_body = request.get_json(force=True)   
        question = json_body["question"]
        app.logger.debug("Question: "+str(question))
        if not question:
            return jsonify({'error': 'No question provided'}), 400
        
        answer  = generate_question(question)
        
        return jsonify({'answer': answer})
    return app

def main():
    app = create_privategpt_server()
    serve(app,host='0.0.0.0',port=5000)
  
if __name__ =='__main__': 
    main()