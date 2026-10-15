"""调用 DeepSeek（OpenAI 兼容接口）。"""

from openai import OpenAI

from config import get_prompt, load_config


def ask(text: str) -> str:
    cfg = load_config()
    client = OpenAI(api_key=cfg["api_key"], base_url=cfg["base_url"])
    resp = client.chat.completions.create(
        model=cfg["model"],
        messages=[
            {"role": "system", "content": get_prompt(cfg)},
            {"role": "user", "content": text},
        ],
    )
    return resp.choices[0].message.content
