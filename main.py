import uvicorn
from fastapi import FastAPI, Response, status
from paddlenlp.transformers import CodeGenTokenizer, CodeGenForCausalLM
from pydantic import BaseModel
from loguru import logger
import time
import paddle
import random
import string


class InputModel(BaseModel):
    prompt: str
    max_tokens: int = 16
    temperature: float = 0.6
    top_k: int = 5
    top_p: float = 1.0
    repetition_penalty: float = 1.1
    use_faster: bool = True
    stream: bool = False


class OutputModel(BaseModel):
    id: str
    model: str = "codegen"
    object: str = "text_completion"
    created: int = int(time.time())
    choices: list = None
    usage = {
        "completion_tokens": None,
        'prompt_tokens': None,
        'total_tokens': None,
    }


def random_completion_id():
    return 'cmpl-' + ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(29))


model_name = 'Salesforce/codegen-350M-mono'
# Init tokenizer
tokenizer = CodeGenTokenizer.from_pretrained(model_name)
# Init model
codegen = CodeGenForCausalLM.from_pretrained(model_name)
logger.info("CodeGenForCausalLM loaded")

app = FastAPI()


@app.post("/v1/engines/codegen/completions", status_code=200)
async def gen(item: InputModel):
    logger.info(item.dict())
    start_time = time.time()
    logger.info("Start generating code")
    inputs = tokenizer([item.prompt])
    inputs = {k: paddle.to_tensor(v) for (k, v) in inputs.items()}
    output, score = codegen.generate(inputs['input_ids'],
                                     max_length=item.max_tokens,
                                     decode_strategy='sampling',
                                     top_k=item.top_k,
                                     repetition_penalty=item.repetition_penalty,
                                     temperature=item.temperature,
                                     use_faster=item.use_faster)
    logger.info("Finish generating code")
    end_time = time.time()
    logger.info("Time cost: {}".format(end_time - start_time))
    output = tokenizer.decode(output[0],
                              skip_special_tokens=True,
                              spaces_between_special_tokens=False)
    output_json = OutputModel(
        id=random_completion_id(),
        choices=[
            {
                "text": output,
                "index": 0,
                "finish_reason": "stop",
                "logprobs": None,
            }
        ],
        usage={
            "completion_tokens": None,
            'prompt_tokens': None,
            'total_tokens': None,
        }
    
    )
    
    if item.stream:
        return Response(status_code=status.HTTP_200_OK, content=output_json.json(),
                        media_type="text/event-stream")
    else:
        return Response(status_code=status.HTTP_200_OK, content=output_json.json(),
                        media_type="application/json")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
