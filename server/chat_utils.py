from typing import List, Any


def parse_chat_history(raw_chat: List[dict[str, Any]]):
    chat_history = []
    for idx, chat_item in enumerate(raw_chat[:-1]):
        next_chat_item = raw_chat[idx + 1]
        if not chat_item["isBot"] and next_chat_item["isBot"]:
            user_input = chat_item["text"]
            bot_response = next_chat_item["text"]
            chat_history.append((user_input, bot_response))

    return chat_history
