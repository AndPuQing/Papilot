import os
from paddlenlp.transformers import CodeGenTokenizer, CodeGenForCausalLM


class Model:
    def __init__(self) -> None:
        env_dist = os.environ
        model_name = env_dist.get("MODEL", "Salesforce/codegen-350M-mono")
        # Init tokenizer
        self.tokenizer = CodeGenTokenizer.from_pretrained(model_name)
        # Init model
        self.codegen = CodeGenForCausalLM.from_pretrained(model_name)
    
    def predict(self, input_ids, **kwargs):
        return self.codegen.generate(input_ids, **kwargs)
    
    def encode(self, text):
        return self.tokenizer([text])
    
    def decode(self, tokens, **kwargs):
        return self.tokenizer.decode(tokens, **kwargs)


CodeGen = Model()
