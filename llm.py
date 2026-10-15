"""调用千问（阿里云百炼）——原生协议，支持联网搜索。"""

import json
import urllib.error
import urllib.request

from config import get_prompt, load_config

ENDPOINT = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"


def ask(text: str) -> str:
    cfg = load_config()
    body = {
        "model": cfg["model"],
        "input": {
            "messages": [
                {"role": "system", "content": get_prompt(cfg)},
                {"role": "user", "content": text},
            ]
        },
        "parameters": {
            "enable_search": bool(cfg.get("web_search", True)),
        },
    }
    req = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {cfg['api_key']}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.load(resp)
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"接口错误 {e.code}: {detail}") from e
    if "output" not in data:
        raise RuntimeError(f"千问返回异常: {data.get('message', data)}")
    return data["output"]["text"].strip()
