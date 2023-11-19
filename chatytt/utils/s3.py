from typing import Dict, Any, List
import json

import boto3


def save_json_to_s3(json_obj: Dict[Any, Any], bucket: str, key: str) -> None:
    s3 = boto3.resource("s3")
    s3_obj = s3.Object(bucket, key)
    s3_obj.put(Body=(bytes(json.dumps(json_obj).encode("UTF-8"))))


def load_json_from_s3_as_dict(bucket: str, key: str) -> Dict[Any, Any]:
    s3 = boto3.resource("s3")
    file_object = s3.Object(bucket, key)
    json_obj = file_object.get()["Body"].read().decode("utf-8")
    dict_obj = json.loads(json_obj)

    return dict_obj


def list_keys_at_prefix_dir_level(bucket: str, filter_prefix_dir: str) -> List[str]:
    s3 = boto3.resource("s3")
    bucket_obj = s3.Bucket(bucket)
    filtered_bucket_obj = bucket_obj.objects.filter(Prefix=f"{filter_prefix_dir}")
    keys = [
        obj.key.replace(filter_prefix_dir, "").split("/")[0]
        for obj in filtered_bucket_obj
    ]

    return list(filter(None, keys))
