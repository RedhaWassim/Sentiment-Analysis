from typing import Dict, Literal, Optional

import pandas as pd
import praw
from praw.models import MoreComments
from praw.models.listing.generator import ListingGenerator
from pydantic import BaseModel, model_validator

from sentiment_analysis.exception import CustomException
from sentiment_analysis.logging_config import logging
from sentiment_analysis.utils.utils import get_from_dict_or_env


class Scrapper(BaseModel):
    scrapping_theme: Literal["hot", "new", "best"]
    """theme to be retreived"""
    topic_number: int
    """how many topics you want"""

    comments_number: int
    """how many comments you want"""

    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    password: Optional[str] = None
    username: Optional[str] = None
    """reddit api_keys"""

    user_agent: Optional[str] = "USER-AGENT"

    class ConfigDict:
        """pydantic forbidding extra arguments"""

        extra = "forbid"

    @model_validator(mode="before")
    @classmethod
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that api key exists in environment."""
        values["client_id"] = get_from_dict_or_env(values, "client_id", "CLIENT_ID")
        values["client_secret"] = get_from_dict_or_env(
            values, "client_secret", "CLIENT_SECRET"
        )
        values["password"] = get_from_dict_or_env(values, "password", "PASSWORD")
        values["username"] = get_from_dict_or_env(values, "username", "USERNAME")

        return values

    def _scrape_data(
        self, scrapper: praw.Reddit, topics: ListingGenerator
    ) -> list[pd.DataFrame]:
        try:
            dfs = []
            for topic in topics:
                data = []
                print(topic)
                post = scrapper.submission(topic)

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

                        data.append([body, date, is_submitter, score, replies_count])

                df = pd.DataFrame(
                    data,
                    columns=["body", "date", "is_submitter", "score", "replies_count"],
                )
                dfs.append(df)

            return dfs
        except Exception as e:
            logging.info("scrapping error")
            raise CustomException(e)

    def run(self) -> list[pd.DataFrame]:
        try:
            scrapper = praw.Reddit(
                client_id=self.client_id,
                client_secret=self.client_secret,
                password=self.password,
                user_agent=self.user_agent,
                username=self.username,
            )

            if self.scrapping_theme == "hot":
                topics = scrapper.front.hot(limit=self.topic_number)
            elif self.scrapping_theme == "new":
                topics = scrapper.front.new(limit=self.topic_number)
            else:
                topics = scrapper.front.best(limit=self.topic_number)

            data = self._scrape_data(scrapper, topics)

            return data
        except Exception as e:
            logging.info("scrapping error")
            raise CustomException(e)

    def __call__(self) -> list[pd.DataFrame]:
        return self.run()
