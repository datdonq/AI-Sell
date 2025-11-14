SCRIPT_PROMPT = f"""
Bạn sẽ được cung cấp thông tin về sản phẩm cần bán, persona của nhân vật livestream, các hành động có thể làm được của nhân vật này
hãy trả về một kịch bản hoàn chỉnh cho buổi livestream này
Output format must be in JSON format with the following keys:
[
{{"content": "string", "action": "string"}}
]
"""