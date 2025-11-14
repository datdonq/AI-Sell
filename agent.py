
import os
import logging
from typing import Dict, Any, List, Optional, Callable, TypeVar, cast
import functools
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, BaseMessage
from langchain_core.tools import tool
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
import dotenv

dotenv.load_dotenv()

import time

def wave_hand():
    """
    Vẫy tay chào
    """
    time.sleep(20)
    return "Vẫy tay chào"
def bow():
    """
    Cúi mình
    """
    time.sleep(20)
    return "Cúi mình"
def jump():
    """
    Nhảy
    """
    time.sleep(20)
    return "Nhảy"
def zoom_in():
    """
    Zoom cận mặt
    """
    time.sleep(20)
    return "Zoom cận mặt"
def shake_hip():
    """
    Lắc hông
    """
    time.sleep(20)
    return "Lắc hông"
def take_photo():
    """
    Tạo dáng chụp hình
    """
    time.sleep(20)
    return "Tạo dáng chụp hình"
def hold_product():
    """
    Cầm sản phẩm
    """
    time.sleep(20)
    return "Cầm sản phẩm"

livestream_agent = create_agent(
        model=ChatGoogleGenerativeAI(model="gemini-2.5-flash", response_mime_type="text/plain", api_key=os.getenv("GEMINI_API_KEY")),
        tools=[wave_hand, bow, jump, zoom_in, shake_hip, take_photo, hold_product],
        system_prompt=('Bạn sẽ được cung cấp hành động và content để livestream, hãy gọi tool tương ứng với hành động'),
    )

query = (
    "Vẫy tay chào"
)

# print(livestream_agent.invoke({"messages": [{"role": "user", "content": query}]}))