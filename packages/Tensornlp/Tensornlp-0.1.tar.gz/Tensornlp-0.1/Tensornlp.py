
class tensorNLP:
    def __init__(self, model, tokenizer, max_len):
        self.model = model
        self.tokenizer = tokenizer
        self.max_len = max_len
        
    def predict(self, text):
        encoded_text = self.tokenizer.encode_plus(
            text,
            add_special_tokens=True,
            max_length=self.max_len,
            return_token_type_ids=False,
            pad_to_max_length=True,
            return_attention_mask=True,
            return_tensors='pt',
        )
        
        input_ids = encoded_text['input_ids']
        attention_mask = encoded_text['attention_mask']
        
        output = self.model(input_ids, attention_mask)
        _, prediction = torch.max(output, dim=1)
        
        return prediction.item()