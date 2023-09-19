import os

import boto3
from supabase import create_client

from sentiment_analysis.data_ingestion.utils.data_processing import (
    insert_comments,
    insert_posts,
    processing,
)
from sentiment_analysis.data_ingestion.utils.json_parser import recursively_parse_json


def lambda_handler(event, context):
    s3_client = boto3.client("s3")
    json_data = recursively_parse_json(event)
    data_list = []

    for record in json_data["Records"]:
        object_key = record["body"]["Message"]["Records"][0]["s3"]["object"]["key"]
        bucket_name = record["body"]["Message"]["Records"][0]["s3"]["bucket"]["name"]

    s3_response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
    content = s3_response["Body"].read().decode("utf-8")

    data_list.append(content)

    posts_df, comments_df = processing(data_list)

    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")

    supabaseClient = create_client(url, key)

    insert_posts(posts_df, supabaseClient)
    insert_comments(comments_df, supabaseClient)
    return {"statusCode": 200, "body": json_data}
