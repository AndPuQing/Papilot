# Papilot

Papilot - 一个基于 PaddleNLP 的开源 GitHub Copilot 服务

## 使用

### 配置

运行 setup 脚本，将会配置使用何种模型以及采用何种方式部署。

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

这将会配置运行环境变量并部署一个 [FastAPI](https://fastapi.tiangolo.com/) 后端服务。

存在 `config.env` 的情况下可以通过`python main.py`启动后端

## API

在上述完成后，将会在`http://0.0.0.0:8000`开启监听服务。你可以通过标准的[OpenAI API](https://beta.openai.com/docs/api-reference/completions/create)进行测试(部分支持)，例如：

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

## Copilot Plugin

就像[fauxpilot](https://github.com/moyix/fauxpilot)一样，我们可以设置 settings.json 来修改 Copilot 插件的后端地址。

```json
    "github.copilot.advanced": {
        "debug.overrideEngine": "codegen",
        "debug.testOverrideProxyUrl": "http://0.0.0.0:8000",
        "debug.overrideProxyUrl": "http://0.0.0.0:8000"
    }
```

## 注意

现在的推理服务的推理速度比较缓慢，所以在`setup.sh`中有一个`LOCK_MAX_TOKENS`的环境变量用于锁定最大的长度，以提高推理的速度。若想体验更强大的补全可以提高该变量值。
