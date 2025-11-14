from typing import Dict
from call_llm import LLMContentGenerator
from dotenv import load_dotenv
from prompt import SCRIPT_PROMPT
from agent import livestream_agent
from comment import get_next_comment
load_dotenv()

def generate_script(product_info: str, persona: str) -> Dict:
    """
    Sinh kịch bản cho buổi livestream
    """
    prompt = f"""
    Thông tin về sản phẩm cần bán: {product_info}
    Persona của nhân vật livestream: {persona}
    Các hành động có thể làm được của nhân vật này: [vẫy tay chào, cúi mình, nhảy, zoom cận mặt, lắc hông, tạo dáng chụp hình, cầm sản phẩm]
    """
    response, token_count = LLMContentGenerator().completion(
        system_prompt=SCRIPT_PROMPT,
        user_prompt=prompt,
        providers=[
            {
                "name": "gemini",
                "model": "gemini-2.5-flash",
                "retry": 3,
                "temperature": 1.5,
                "top_k": 40,
                "top_p": 0.95,
                "thinking_budget": 10000,
            }
        ],
        json=True,
    )
    return response

if __name__ == "__main__":
    product_info = "Sản phẩm là một chiếc áo sơ mi nam trắng, size L, giá 100.000 VNĐ"
    persona = "Nhân vật livestream là một người đàn ông trung niên, cao 170cm, nặng 70kg, mặt trắng, tóc đen, mắt đen, mũi đen, môi đen"
    script = generate_script(product_info, persona)
    for action in script:
        # Thực hiện action trong kịch bản
        print(livestream_agent.invoke({"messages": [{"role": "user", "content": action["action"]}]}))
        # Sau khi action kết thúc, xử lý toàn bộ comment đang chờ (nếu có)
        while True:
            comment_text = get_next_comment()
            if not comment_text:
                break
            print(livestream_agent.invoke({"messages": [{"role": "user", "content": comment_text}]}))