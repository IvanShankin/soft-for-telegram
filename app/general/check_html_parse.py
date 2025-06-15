from bs4 import BeautifulSoup
import re


def check_html_parse(text: str) -> bool:
    """Проверяет корректность HTML-разметки для Telegram.
    Возвращает True, если разметка верна, иначе False.
    """
    ALLOWED_TAGS = {"b", "i", "u", "s", "a", "code", "pre"}

    # Проверка на незакрытые/перекрытые теги через стек
    stack = []
    for tag in re.finditer(r"<\/?([a-zA-Z]+)[^>]*>", text):
        tag_name = tag.group(1).lower()
        is_open_tag = not tag.group(0).startswith("</")

        if is_open_tag:
            if tag_name not in ALLOWED_TAGS:
                return False
            stack.append(tag_name)
        else:
            if not stack or stack.pop() != tag_name:
                return False

    if stack:  # Остались незакрытые теги
        return False

    # Дополнительная проверка через BeautifulSoup
    try:
        soup = BeautifulSoup(text, "html.parser")

        # Проверяем валидность тегов и атрибутов
        for tag in soup.find_all(True):
            if tag.name.lower() not in ALLOWED_TAGS:
                return False
            if tag.name == "a" and not tag.get("href"):
                return False

        return True
    except Exception:
        return False