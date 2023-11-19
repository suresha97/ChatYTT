from typing import Any
import json


def write_data_to_json_file(data: Any, file_name: str):
    with open(file_name, "w") as file:
        json.dump(data, file)


def read_data_from_json_file(file_path: str) -> dict:
    with open(file_path, "r") as file:
        data = json.load(file)

    return data


def write_data_to_txt_file(data: Any, file_name: str):
    with open(file_name, "w") as file:
        file.write(data)
