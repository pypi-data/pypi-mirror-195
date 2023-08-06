import torch.nn as nn
from transformers import BertModel, BertPreTrainedModel

class BertClassifier(BertPreTrainedModel):
    def __init__(self, config):
        super().__init__(config)
        self.bert = BertModel(config)
        self.linear = nn.Linear(config.hidden_size, 1)
        
    def forward(self, input_ids, attention_mask, token_type_ids):
        top_vec = self.bert(input_ids=input_ids, token_type_ids=token_type_ids, attention_mask=attention_mask)[0]
        cls_vec = top_vec[:, 0, :]
        logits = self.linear(cls_vec).squeeze(-1)
        return logits