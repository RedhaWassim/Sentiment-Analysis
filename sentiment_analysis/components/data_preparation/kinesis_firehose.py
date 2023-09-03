import boto3 
import json
import pydantic 
from pydantic import BaseModel, model_validator
from sentiment_analysis.utils.utils import get_from_dict_or_env
from bson import json_util
from typing import Dict, Literal, Optional,Any

class MetaClass:

    _instance={}

    def __call__(cls,*args,**kwargs):
        """lmit number of instances to 1"""

        if cls not in cls._instance:
            cls._instance[cls]=super(MetaClass,cls).__call__(*args,**kwargs)
            return cls._instance
    pass


class KinesisFireHose(BaseModel):
    access_key_id: Optional[str] = None
    secret_access_key: Optional[str] = None
    stream_name: str 
    client : Optional[Any] = None
    class ConfigDict:
        """pydantic forbidding extra arguments"""

        extra = "allow"
    
    
    @model_validator(mode="before")
    @classmethod
    def initialize_client(cls, values: Dict) -> Dict:
        """Initialize the client after API keys are validated."""
        client =boto3.client('firehose', region_name='eu-north-1',
                                        aws_access_key_id=values["access_key_id"],
                                        aws_secret_access_key=values["secret_access_key"])
        values["client"] = client
        return values
    
    @model_validator(mode="before")
    @classmethod
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that api key exists in environment."""
        values["access_key_id"] = get_from_dict_or_env(values, "access_key_id", "AWS_ACCESS_KEY_ID")
        values["secret_access_key"] = get_from_dict_or_env(values, "secret_access_key", "AWS_SECRET_ACCESS_KEY")
        

        return values
    
    @property
    def describe(self):
        """
        give information about the kinesis firehose
        
        returns : 
            json
        """
        response=self.client.describe_delivery_stream(
            DeliveryStreamName=self.stream_name
        )
        response_json=json.dumps(response,
                                indent=4,
                                default=json_util.default
                                )        
        return response_json
    

    def post(self,payload=None):
        """"
        args : 
            payload : dict or json payload to upload on kinesis

        return :

            json response from aws

        """

        json_payload=json.dumps(payload)
        json_payload =json_payload+ "\n"

        json_payload_encoded=json_payload.encode("UTF-8")


        response=self.client.put_record(
            DeliveryStreamName=self.stream_name,
            Record={"data":json_payload_encoded}

        )

        response_aws=json.dumps(response,indent=3)
        return response        



