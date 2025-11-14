import json
import os
import time
from datetime import datetime
from typing import List, Optional

# Simple file-based queue for simulating user comments
_ROOT_DIR = os.path.dirname(__file__)
_QUEUE_FILE = os.path.join(_ROOT_DIR, "comments_queue.jsonl")
_OFFSET_FILE = os.path.join(_ROOT_DIR, "comments_offset.txt")


def _ensure_files() -> None:
    if not os.path.exists(_QUEUE_FILE):
        with open(_QUEUE_FILE, "a", encoding="utf-8"):
            pass
    if not os.path.exists(_OFFSET_FILE):
        with open(_OFFSET_FILE, "w", encoding="utf-8") as f:
            f.write("0")


def enqueue_comment(comment: str) -> None:
    """
    Thêm một comment vào hàng đợi (append vào file JSONL)
    """
    _ensure_files()
    record = {
        "comment": comment,
        "created_at": datetime.utcnow().isoformat() + "Z",
    }
    with open(_QUEUE_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def enqueue_comments(comments: List[str], delay_seconds: float = 0.0) -> None:
    """
    Thêm lần lượt nhiều comment vào hàng đợi.
    delay_seconds > 0 để mô phỏng người dùng nhập từng cái theo thời gian.
    """
    for c in comments:
        enqueue_comment(c)
        if delay_seconds > 0:
            time.sleep(delay_seconds)


def get_next_comment() -> Optional[str]:
    """
    Lấy comment tiếp theo chưa xử lý (dựa trên con trỏ offset).
    Trả về None nếu không có comment mới.
    """
    _ensure_files()
    try:
        with open(_OFFSET_FILE, "r+", encoding="utf-8") as f_offset:
            raw = f_offset.read().strip()
            offset = int(raw) if raw else 0

        with open(_QUEUE_FILE, "r", encoding="utf-8") as f_queue:
            lines = f_queue.readlines()

        if offset >= len(lines):
            return None

        line = lines[offset].strip()
        try:
            data = json.loads(line)
            comment_text = data.get("comment", "").strip()
        except Exception:
            comment_text = ""

        # Cập nhật offset ngay khi đã đọc dòng này
        with open(_OFFSET_FILE, "w", encoding="utf-8") as f_offset:
            f_offset.write(str(offset + 1))

        return comment_text or None
    except Exception:
        return None


if __name__ == "__main__":
    # Demo: hard-code một danh sách comment và đẩy lần lượt vào hàng đợi
    demo_comments = [
        "Zoom cận mặt giúp tôi xem rõ hơn",
        "Hãy vẫy tay chào khán giả mới vào",
        "Cúi mình cảm ơn",
        "Nhảy một điệu vui nhộn",
    ]
    # Đẩy mỗi comment cách nhau 2 giây để mô phỏng
    enqueue_comments(demo_comments, delay_seconds=2.0)
    print("Đã đẩy demo comments vào hàng đợi.")

