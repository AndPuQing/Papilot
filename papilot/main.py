import uvicorn
from fastapi import FastAPI, Response, status
from pydantic import BaseModel
from loguru import logger
import time
import paddle
import random
import string
import json
import os
from sse_starlette.sse import EventSourceResponse
from dotenv import load_dotenv, find_dotenv
from model import CodeGen


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
        "prompt_tokens": None,
        "total_tokens": None,
    }


def random_completion_id():
    return "cmpl-" + "".join(
        random.choice(string.ascii_letters + string.digits) for _ in range(29)
    )


load_dotenv(find_dotenv(filename="config.env"), override=True)

env_dist = os.environ

app = FastAPI()


@app.post("/v1/engines/codegen/completions", status_code=200)
async def gen(item: InputModel):
    logger.info("Request: {}".format(item.dict()))

    if item.temperature == 0.0:
        item.temperature = 1.0
        item.top_k = 1

    start_time = time.time()
    logger.info("Start generating code")
    inputs = CodeGen.encode(item.prompt)
    inputs = {k: paddle.to_tensor(v) for (k, v) in inputs.items()}
    output, score = CodeGen.predict(
        inputs["input_ids"],
        max_length=int(env_dist.get("TOKEN_LENGTH", item.max_tokens)),
        decode_strategy="sampling",
        top_k=item.top_k,
        repetition_penalty=item.repetition_penalty,
        temperature=item.temperature,
        use_faster=item.use_faster,
    )
    logger.info("Finish generating code")
    end_time = time.time()
    logger.info("Time cost: {}".format(end_time - start_time))
    output = CodeGen.decode(
        output[0], skip_special_tokens=True, spaces_between_special_tokens=False
    )
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
            "prompt_tokens": None,
            "total_tokens": None,
        },
    )

    def stream_response(response):
        yield f"{json.dumps(response)}\n\n"
        yield "data: [DONE]\n\n"

    if item.stream:
        return EventSourceResponse(stream_response(output_json.dict()))
    else:
        return Response(
            status_code=status.HTTP_200_OK,
            content=output_json.json(),
            media_type="application/json",
        )


def main():
    uvicorn.run("main:app", host="0.0.0.0", port=int(env_dist.get("PORT", 8000)))


if __name__ == "__main__":
    main()
