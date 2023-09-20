from typing import Any, Dict, Literal, Optional

import pandas as pd
import praw
from praw.models import MoreComments
from praw.models.listing.generator import ListingGenerator
from pydantic import model_validator

from sentiment_analysis.data_pipeline.processing.kinesis_firehose.kinesis_firehose import (
    KinesisFireHose,
)
from sentiment_analysis.exception import CustomException
from sentiment_analysis.logging_config import logging
from sentiment_analysis.utils.utils import get_from_dict_or_env


class Topic_producer(KinesisFireHose):
    scrapping_theme: Literal["hot", "new", "best"]
    """theme to be retreived"""
    topic_number: int
    """how many topics you want"""

    comments_number: int
    """how many comments you want"""

    producer: Optional[Any] = None
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    password: Optional[str] = None
    username: Optional[str] = None
    """reddit api_keys"""

    # supabase_url : Optional[str] = None
    # supabase_key : Optional[str] = None
    """database key"""

    user_agent: Optional[str] = "user_agent"

    scrapper: Optional[Any] = None

    class ConfigDict:
        """pydantic forbidding extra arguments"""

        extra = "forbid"

    @model_validator(mode="before")
    @classmethod
    def validate_environment_scrapper(cls, values: Dict) -> Dict:
        """Validate that api key exists in environment."""
        values["client_id"] = get_from_dict_or_env(values, "client_id", "CLIENT_ID")
        values["client_secret"] = get_from_dict_or_env(
            values, "client_secret", "CLIENT_SECRET"
        )
        values["password"] = get_from_dict_or_env(values, "password", "PASSWORD")
        values["username"] = get_from_dict_or_env(values, "username", "USERNAME")

        scrapper = praw.Reddit(
            client_id=values["client_id"],
            client_secret=values["client_secret"],
            password=values["password"],
            user_agent=cls.model_fields["user_agent"].default,
            username=values["username"],
        )

        values["scrapper"] = scrapper

        return values

    def _comment_producer(self, scrapper: praw.Reddit, post) -> list[Dict[str, Any]]:
        """
        Args:

        scrapper : the scrapper instance
        post : the reddit submission where you want to scrappe comments

        return:
          list of comments
        """
        try:
            comments_list = []

            comments = post.comments
            for comment in comments[1 : self.comments_number + 1]:
                if isinstance(comment, MoreComments):
                    pass
                else:
                    body = comment.body
                    date = comment.created_utc
                    is_submitter = comment.is_submitter
                    score = comment.score
                    replies = comment.replies
                    replies_count = len(replies)
                    id = comment.id
                    json = {
                        "id": id,
                        "body": body,
                        "date": date,
                        "is_submitter": is_submitter,
                        "score": score,
                        "replies_count": replies_count,
                    }

                    comments_list.append(json)

            return comments_list

        except Exception as e:
            logging.info("scrapping error")
            raise CustomException(e)

    def _topic_producer(
        self, scrapper: praw.Reddit, topics: ListingGenerator
    ) -> list[Dict[str, Any]]:
        try:
            data = []
            for topic in topics:
                post = scrapper.submission(topic)

                post_id = post.id
                title = post.title
                date = post.created_utc
                score = post.score
                num_comments = post.num_comments
                upvote_ratio = post.upvote_ratio
                over_18 = post.over_18
                id = post_id.id

                value = {
                    "id": id,
                    "TITLE": title,
                    "POST_DATE": date,
                    "SCORE": score,
                    "NUM_COMMENTS": num_comments,
                    "UPVOTE_RATIO": upvote_ratio,
                    "OVER_18": over_18,
                    "COMMENTS": self._comment_producer(scrapper, post),
                }
                self.post(value)
                print(topic, "posted successfully")

                data.append(value)

            return data

        except Exception as e:
            logging.info("scrapping error")
            raise CustomException(e)

    def run(self):
        try:
            if self.scrapping_theme == "hot":
                topics = self.scrapper.front.hot(limit=self.topic_number)
            elif self.scrapping_theme == "new":
                topics = self.scrapper.front.new(limit=self.topic_number)
            else:
                topics = self.scrapper.front.best(limit=self.topic_number)

            return self._topic_producer(self.scrapper, topics)

        except Exception as e:
            logging.info("scrapping error")
            raise CustomException(e)

    def __call__(self) -> list[pd.DataFrame]:
        return self.run()


def main():
    scrapper = Topic_producer(scrapping_theme="hot", topic_number=2, comments_number=4)
    print(scrapper)


if __name__ == "__main__":
    main()
