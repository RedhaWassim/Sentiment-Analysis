Reddit Posts Sentiment Analysis
## Overview

The Reddit Posts Sentiment Analysis project aims to provide a tool for analyzing the sentiment of a post based on the comments . The project leverages natural language processing and machine learning techniques to determine whether the comments  are positive, negative, or neutral in sentiment and assign the sentiment to the original post .

## Features

- Batch data collection: The system collects posts and comments in batchs based on best / new / tranding topics.
- Sentiment analysis: posts and comments are analyzed using a machine learning model to determine their sentiment.
- Interactive dashboard: Visualizes sentiment trends over time for different topics.

<h1 align="center">
FULL PROJECT WORKFLOW
</h1>

this project is devided into 3 main parts: 

- Data part : Responsible for scrapping , processing , storing the raw data into a database. 
- Model part : Responsible for ingesting data from database , processing and passing data into the machine learning model to get sentiment.
- Analyse part : Responsible for analyse results and data .  

![project_workflow](https://github.com/RedhaWassim/Sentiment-Analysis/assets/78182178/b77a6769-b6a7-4169-a893-88f643b01b8c)

<h1 align="center">
DATA PART
</h1>

- data ingestion  : this module is reponsible for scrapping data from reddit using : PRAW library .
- AWS Module :

  
     - Data Retreiver : Using AWS Kinesis firehose i can ingest data in batches into the S3 Bucket.
     - Data Storage : Using the data lake S3 , i can store all the raw data.
     - Data Processing :

        1. Using AWS SNS for notifications when data is inputed into the S3 bucket.

        2. Using AWS SQS for queue system.                     

        3. Using AWS LAMBDA ( python ) for data processing.
           
- Data storage : Using SUPABASE as SQL database to store the processsed data into 2 tables : POSTS , COMMENTS . 


![3](https://github.com/RedhaWassim/Sentiment-Analysis/assets/78182178/365e547c-f353-4230-8857-d6c5d299ca47)

<h1 align="center">
MODEL PART
</h1>

### plan
model V1 : 
![Colorful Minimalist Linear Steps Circular Diagram (2048 × 768 px) (2048 × 1080 px) (2048 × 900 px) (2048 × 850 px) (1200 × 850 px) (2500 × 850 px) (2500 × 1024 px)](https://github.com/RedhaWassim/Sentiment-Analysis/assets/78182178/41ffd154-fa87-42fc-849b-2469248b88c5)


#### current plan : 

- using semi-supervised method , by public reddit texts data i can train a model to predict the sentiment .
- i will use this model to generate pseudo-labels for my data
- I adopt a multi-input neural network architecture.
- I begin by saving the knowledge from the pre-trained model's hidden layers and freezing them.
- I add features and columns that are unique to my dataset by constructing a new hidden layer dedicated to process those informations.
- To combine the insights from both text and the additional columns, I've added a special layer that effortlessly merges the knowledge from the pre-trained layers and the new columns layer.
  
## Todo

### Data pipeline
- [x] ~~configure~~
- [x] ~~data collection~~
- [x] ~~data processing~~
- [x] ~~data storage~~

### ML pipeline
- [x] ~~data ingestion~~
- [x] ~~data transformation~~
- [ ] model training  , evaluation , tuning
- [ ] Deploy,Monitoring

### Testing 
- [ ] add unit tests
- [ ] add integration tests

## ideas:


## Contact

- Your Name: [bra.rwassim@gmail.com]
- Project Link: [https://github.com/RedhaWassim/end-to-end-real-time-twitter-sentiment-analysis]
- LinkedIn: [https://www.linkedin.com/in/redha-wassim-brahimi-67a526224/]
