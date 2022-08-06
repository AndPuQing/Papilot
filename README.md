English | [简体中文](./README_cn.md)

# Papilot

Papilot - an open-source GitHub Copilot server based PaddleNLP

## Uses

### setup

run the setup script. The inference model will be configured and how it will be deployed.

```shell
Models available:
[1] codegen-350M-mono (2GB total VRAM required; Python-only)
[2] codegen-350M-multi (2GB total VRAM required; multi-language)
[3] codegen-2B-mono (7GB total VRAM required; Python-only)
[4] codegen-2B-multi (7GB total VRAM required; multi-language)
[5] codegen-6B-mono (13GB total VRAM required; Python-only)
[6] codegen-6B-multi (13GB total VRAM required; multi-language)
[7] codegen-16B-mono (32GB total VRAM required; Python-only)
[8] codegen-16B-multi (32GB total VRAM required; multi-language)
Enter your choice [1]:
Enter number of GPUs [1]:
Deployment method:
[1] Deploy to Docker
[2] Deploy to localhost
Where do you want to deploy the Papilot [localhost]?
Port [8000]:
lock_max_tokens [16]:  LOCK_MAX_TOKENS
Deploying to localhost
install dependencies......
...
INFO:     Started server process [1116]
INFO 2022-08-05 18:52:50,595 server.py:75] Started server process [1116]
INFO:     Waiting for application startup.
INFO 2022-08-05 18:52:50,596 on.py:47] Waiting for application startup.
INFO:     Application startup complete.
INFO 2022-08-05 18:52:50,596 on.py:61] Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO 2022-08-05 18:52:50,599 server.py:207] Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

This will configure the runtime environment variables and deploy a [FastAPI](https://fastapi.tiangolo.com/) backend service.

> The backend can be started via `python main.py` if `config.env` exists

## API

After the above is completed, the listening service will be started at `http://0.0.0.0:8000`. You can test (partially supported) through the standard [OpenAI API](https://beta.openai.com/docs/api-reference/completions/create), for example:

```python
$ ipython

Python 3.9.12 (main, Jun  1 2022, 11:38:51)
Type 'copyright', 'credits' or 'license' for more information
IPython 8.4.0 -- An enhanced Interactive Python. Type '?' for help.

In [1]: import openai

In [2]: openai.api_key = 'dummy'

In [3]: openai.api_base = 'http://127.0.0.1:8000/v1'

In [4]: result = openai.Completion.create(engine='codegen', prompt='def hello', max_tokens=16, temperature=0.1)

In [5]: result
Out[5]:
<OpenAIObject text_completion id=cmpl-dmhoeHmcw9DJ4NeqOJDQVKv3iivJ0 at 0x7fe7a81d42c0> JSON: {
  "choices": [
    {
      "finish_reason": "stop",
      "index": 0,
      "logprobs": null,
      "text": "_world():\n    print(\"Hello World!\")\n\n\n#"
    }
  ],
  "created": 1659699508,
  "id": "cmpl-dmhoeHmcw9DJ4NeqOJDQVKv3iivJ0",
  "model": "codegen",
  "object": "text_completion",
  "usage": {
    "completion_tokens": null,
    "prompt_tokens": null,
    "total_tokens": null
  }
}
```

Or test via swagger at http://0.0.0.0:8000/docs

## Copilot Plugin

Just like [fauxpilot](https://github.com/moyix/fauxpilot) we can set `settings.json` to modify the backend address of the Copilot plugin.

> Unfortunately, no relevant documentation was found. Only this [discuss](https://github.com/community/community/discussions/19537) is relevant

```json
    "github.copilot.advanced": {
        "debug.overrideEngine": "codegen",
        "debug.testOverrideProxyUrl": "http://0.0.0.0:8000",
        "debug.overrideProxyUrl": "http://0.0.0.0:8000"
    }
```

## Notes

The inference speed of the current inference service is relatively slow, so there is a `LOCK_MAX_TOKENS` environment variable in `setup.sh` to lock the maximum length to improve the inference speed. If you want to experience more powerful completion, you can increase the value of this variable.

## Acknowledge

This repo references the [FauxPilot](https://github.com/moyix/fauxpilot) repo, without his work there would be no following. Thank.
