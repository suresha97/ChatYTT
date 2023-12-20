import time
from typing import List, Any

import boto3

table = boto3.resource("dynamodb").Table("chatytt-chat-history")


def fetch_chat_history(user_id: str):
    response = table.get_item(Key={"UserId": user_id})
    return response["Item"]


def is_new_user(user_id: str) -> bool:
    response = table.get_item(Key={"UserId": user_id})
    return response.get("Item") is None


def update_chat_history(user_id: str, chat_history: List[dict[str, Any]]):
    if is_new_user(user_id):
        create_chat_history(user_id=user_id, chat_history=chat_history)
    else:
        chat_history_update_data = {
            "UpdatedTimestamp": {"Value": int(time.time()), "Action": "PUT"},
            "ChatHistory": {"Value": chat_history, "Action": "PUT"},
        }
        table.update_item(
            Key={"UserId": user_id}, AttributeUpdates=chat_history_update_data
        )


def create_chat_history(user_id: str, chat_history: List[dict[str, Any]]):
    item = {
        "UserId": user_id,
        "CreatedTimestamp": int(time.time()),
        "UpdatedTimestamp": None,
        "ChatHistory": chat_history,
    }
    table.put_item(Item=item)
