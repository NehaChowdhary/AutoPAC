import pytorch_lightning as pl
from transformers import T5ForConditionalGeneration
from transformers import AdamW
import os

class T5Model(pl.LightningModule):
    def __init__(self):
        super().__init__()
        self.MODEL_NAME=os.environ.get("MODEL_NAME")
        self.model = T5ForConditionalGeneration.from_pretrained(self.MODEL_NAME, return_dict = True)

        
    def forward(self, input_ids, attention_mask, labels=None):
        output = self.model(
        input_ids=input_ids, 
        attention_mask=attention_mask, 
        labels=labels
        )
        return output.loss, output.logits
    
    def training_step(self, batch, batch_idx):

        input_ids = batch["input_ids"]
        attention_mask = batch["attention_mask"]
        labels= batch["target"]
        loss, logits = self(input_ids , attention_mask, labels)

        
        self.log("train_loss", loss, prog_bar=True, logger=True)

        return {'loss': loss}
    
    def validation_step(self, batch, batch_idx):
        input_ids = batch["input_ids"]
        attention_mask = batch["attention_mask"]
        labels= batch["target"]
        loss, logits = self(input_ids, attention_mask, labels)

        self.log("val_loss", loss, prog_bar=True, logger=True)
        
        return {'val_loss': loss}

    def configure_optimizers(self):
        return AdamW(self.parameters(), lr=0.0001)
