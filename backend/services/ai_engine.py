"""
AI 关联引擎：调用 Gemini API 生成作家-事件深层关联
"""
import os
import google.generativeai as genai

_client = None


def _get_client():
    global _client
    if _client is None:
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        _client = genai.GenerativeModel("gemini-2.0-flash")
    return _client


PROMPT_TEMPLATE = """\
你是一位精通文学史与世界历史的学者。

作家：{name_zh}（{birth}{death_str}，{nationality}）
历史事件：{year}年，{event_zh}
关联类型：{relation_type_desc}

请用200字以内的中文，阐述这位作家与这一历史事件之间的深层关联。
要求：
1. 分析事件对作家创作的具体影响（或作家对事件的回应）
2. 引用作家具体作品或言论作为佐证
3. 语言生动，避免泛泛而谈
4. 若两者之间无显著关联，请如实说明

最后一行请用以下格式输出置信度（0.00~1.00）：
CONFIDENCE: 0.85\
"""

RELATION_DESC = {
    "influence": "历史事件直接影响了作家的创作题材、风格或人生轨迹",
    "response":  "作家通过作品或言论直接回应了该事件",
    "parallel":  "事件与作家的某部作品在主题或时间上形成平行共鸣",
    "contrast":  "事件与作家的世界形成鲜明对照，产生张力",
}


async def generate_link(author, event, relation_type: str) -> dict:
    death_str = f"-{author.death}" if author.death else "-至今"
    prompt = PROMPT_TEMPLATE.format(
        name_zh=author.name_zh,
        birth=author.birth,
        death_str=death_str,
        nationality=author.nationality,
        year=event.year,
        event_zh=event.event_zh,
        relation_type_desc=RELATION_DESC.get(relation_type, relation_type),
    )

    client = _get_client()
    response = await client.generate_content_async(prompt)
    full_text: str = response.text
    lines = full_text.strip().splitlines()

    # 提取置信度
    confidence = 0.80
    annotation_lines = []
    for line in lines:
        if line.startswith("CONFIDENCE:"):
            try:
                confidence = float(line.split(":")[1].strip())
            except ValueError:
                pass
        else:
            annotation_lines.append(line)

    annotation = "\n".join(annotation_lines).strip()
    summary = annotation[:60] + "…" if len(annotation) > 60 else annotation

    return {
        "summary":    summary,
        "annotation": annotation,
        "confidence": confidence,
        "model":      "gemini-2.0-flash",
        "prompt":     prompt,
        "tokens":     0,
    }
