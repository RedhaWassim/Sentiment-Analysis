# Real-Time Twitter Sentiment Analysis
## Overview

The Real-Time Twitter Sentiment Analysis project aims to provide a tool for analyzing the sentiment of tweets related to trending topics on Twitter. The project leverages natural language processing and machine learning techniques to determine whether tweets are positive, negative, or neutral in sentiment.

## Features

- Real-time data collection: The system collects tweets in real-time based on trending topics.
- Sentiment analysis: Tweets are analyzed using a machine learning model to determine their sentiment.
- Interactive dashboard: Visualizes sentiment trends over time for different topics.
- User-friendly interface: Provides an easy-to-use interface for users to interact with the tool.

## Todo

- [x] ~~configure~~
- [x] ~~data collection~~
- [ ] data processing
- [ ] data storage
- [ ] models
- [ ] Deploy
- [ ] Monitoring
- [ ] Add tests


## Actual:

### Redha

[] put scrapped data in supabase


## ideas:
-analyse the data and do visualisation for:  

    -r/


    -time of comments 


    -relationship between time of tweets and the sentiment 


    -relationship between r/ and the sentiment 

-make 2 DB 


    -premiere : unlabeled , use unsupervised learning to do sentiment analysis


    -deuxiemme : utiliser un LLM pour labeliser les donner , puis utiliser un supervised learning model 


-avec assez de données , essayer de faire un fine tuning d'un petit LLM et voir le resultat 

- Database backup with AWS S3

-faire une liste de users qui ont beaucoup de likes , faire une analyse sur les posts de ces users et voir  

-ajouter l'attribut saison pour voir si la saison influence les emotions

-potentielement enlever l'attribut "posted date" et mettre ca en 2 : 
    -saison
    -matin/aprem/soir/nuit 

-bot dans reddit pour lancer directement l'execution avec une simple commande 

## Contact

- Your Name: [bra.rwassim@gmail.com]
- Project Link: [https://github.com/RedhaWassim/end-to-end-real-time-twitter-sentiment-analysis]
- LinkedIn: [https://www.linkedin.com/in/redha-wassim-brahimi-67a526224/]