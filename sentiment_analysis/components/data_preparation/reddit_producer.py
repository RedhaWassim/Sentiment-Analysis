from typing import Dict, Literal, Optional,Any
import pandas as pd
import praw
from praw.models import MoreComments
from praw.models.listing.generator import ListingGenerator
from pydantic import BaseModel, model_validator

from sentiment_analysis.exception import CustomException
from sentiment_analysis.logging_config import logging
from sentiment_analysis.utils.utils import get_from_dict_or_env

from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.serialization import StringSerializer
from confluent_kafka import SerializingProducer
from confluent_kafka.schema_registry.avro import AvroSerializer

from sentiment_analysis.components.data_preparation.config import my_api_keys

class Topic_producer(BaseModel):
    scrapping_theme: Literal["hot", "new", "best"]
    """theme to be retreived"""
    topic_number: int
    """how many topics you want"""

    comments_number: int
    """how many comments you want"""

    producer: Optional[Any]= None
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    password: Optional[str] = None
    username: Optional[str] = None
    """reddit api_keys"""

    kafka_config : Optional[Dict] =None
    """kafka_config"""


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

    def comment_producer(
        self, scrapper: praw.Reddit, topics: ListingGenerator
    ) -> Dict:
        try:
            data = []
            for topic in topics:
                json = {}
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

                        json={"body" :body,
                              "date":date,
                              "is_submitter":is_submitter,
                              "score":score,
                              "replies_count":replies_count}

                data.append(json)

            return data
        except Exception as e:
            logging.info("scrapping error")
            raise CustomException(e)
        
    
    def on_delivery(self,err,record):
        pass

    def topic_producer(
        self, scrapper: praw.Reddit, topics: ListingGenerator
    ) -> Dict:
        try:
            data = []
            for topic in topics:
                json = {}
                print(topic)
                post = scrapper.submission(topic)

                post_id=post.id
                title = post.title
                date = post.created_utc
                score = post.score
                num_comments = post.num_comments
                upvote_ratio=post.upvote_ratio
                over_18=post.over_18
                id=post_id.id
                
                self.producer.produce(topic="reddit_topics",
                    key=id,
                    value={
                    "TITLE" : title,
                    "POST_DATE":date,
                    "SCORE":score,
                    "NUM_COMMENTS":num_comments,
                    "UPVOTE_RATIO":upvote_ratio,
                    "OVER_18":over_18,
                    },
                    on_delivery=self.on_delivery,
                )

            self.producer.flush()             
            
        except Exception as e:
            logging.info("scrapping error")
            raise CustomException(e)


    def run(self):
        try:
            scrapper = praw.Reddit(
                client_id=self.client_id,
                client_secret=self.client_secret,
                password=self.password,
                user_agent=self.user_agent,
                username=self.username,
            )
            api_keys=my_api_keys()

            schema_registery_client = SchemaRegistryClient(api_keys.schema_registry)
            reddit_post_value_schema=schema_registery_client.get_latest_version("reddit_topics-value")

            config=api_keys.KAFKA_CONFIG | {
                "key.serializer": StringSerializer(),
                "value.serializer": AvroSerializer(schema_registery_client,
                                                   reddit_post_value_schema.schema.schema_str),
            }
            self.producer=SerializingProducer(config)

            if self.scrapping_theme == "hot":
                topics = scrapper.front.hot(limit=self.topic_number)
            elif self.scrapping_theme == "new":
                topics = scrapper.front.new(limit=self.topic_number)
            else:
                topics = scrapper.front.best(limit=self.topic_number)


            self.topic_producer(scrapper,topics)
        
        except Exception as e:
            logging.info("scrapping error")
            raise CustomException(e)

    def __call__(self) -> list[pd.DataFrame]:
        self.run()
 
