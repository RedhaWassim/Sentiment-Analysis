from sentiment_analysis.components.data_preparation.data_scrapping import Scrapper
import pandas as pd
def test_scrapper():
    scrapper=Scrapper(scrapping_theme="new",topic_number=1,comments_number=1)

    data=scrapper()

    assert isinstance(scrapper.topic_number,int)
    assert isinstance(scrapper.comments_number,int)
    assert scrapper.scrapping_theme=="new"
    assert isinstance(data,list[pd.DataFrame])