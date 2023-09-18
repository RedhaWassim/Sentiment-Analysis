import datetime

import pandas as pd
from json_parser import recursively_parse_json


def data_splitting(data):
    posts_data = []
    comments_data = []
    json_objects = data[0].strip().split("\n")
    data = recursively_parse_json(json_objects)
    for post in data:
        post_copy = {key: value for key, value in post.items() if key != "COMMENTS"}
        comments = post["COMMENTS"]
        id = post["id"]
        for comment in comments:
            comment["post_id"] = id

        posts_data.append(post_copy)
        comments_data.extend(comments)

    posts_df = pd.DataFrame(posts_data)
    comments_df = pd.DataFrame(comments_data)

    return posts_df, comments_df


def date_time_processing(date):
    date_time = datetime.datetime.fromtimestamp(date)
    year = date_time.year
    month = date_time.month
    day = date_time.day
    hour = date_time.hour

    return year, month, day, hour


def comment_processing(comment):
    comment["body"] = comment["body"].lower()
    comment["is_submitter"] = int(comment["is_submitter"])
    timestamp = comment["date"]
    year, month, day, hour = date_time_processing(timestamp)
    comment["YEAR"] = year
    comment["MONTH"] = month
    comment["DAY"] = day
    comment["HOUR"] = hour
    return comment


def post_processing(post):
    post["TITLE"] = post["TITLE"].lower()
    post["OVER_18"] = int(post["OVER_18"])
    timestamp = post["POST_DATE"]
    year, month, day, hour = date_time_processing(timestamp)
    post["YEAR"] = year
    post["MONTH"] = month
    post["DAY"] = day
    post["HOUR"] = hour
    return post


def processing(data):
    posts_df, comments_df = data_splitting(data)
    posts_df = posts_df.apply(lambda x: post_processing(x), axis=1)
    comments_df = comments_df.apply(lambda x: comment_processing(x), axis=1)

    return posts_df, comments_df


def insert_posts(posts_df, supabase):
    for idx, row in posts_df.iterrows():
        try:
            row = row.to_json()

            json_data = recursively_parse_json(row)

            data, count = supabase.table("POSTS").insert(json_data).execute()
        except Exception as e:
            print(e)
            pass


def insert_comments(comments_df, supabase):
    for idx, row in comments_df.iterrows():
        try:
            row = row.to_json()

            json_data = recursively_parse_json(row)
            data, count = supabase.table("COMMENTS").insert(json_data).execute()
        except Exception as e:
            print(e)
            pass
