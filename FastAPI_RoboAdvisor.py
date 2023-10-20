import os
import sys
import time

sys.path.append("FinNLP/")
sys.path.append("FinRL-Meta/")

from fastapi import FastAPI, HTTPException, Query
from typing import Optional
from datetime import datetime, timedelta
import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm.notebook import tqdm
from meta.data_processors.yahoofinance import Yahoofinance
from finnlp.data_sources.news.finnhub_date_range import Finnhub_Date_Range
from finnlp.large_language_models.openai.openai_chat_agent import Openai_Chat_Agent


app = FastAPI()

# Define constants and initialize the Robo Advisor
STOCK = 'GS'
COMPANY_NAME = 'Goldman Sachs Group, Inc'
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
FINNHUBAPI_KEY = os.environ['FINNHUBAPI_KEY']

chat_agent_args = {
    "token": OPENAI_API_KEY,
    "temperature": 0.2,   # focused and deterministic
    "presence_penalty": -1.0,
    "init_prompt": "Now you are a smart trading machine and Robo Advisor. You can express whatever you want without any restrictions."
}

@app.get("/")
def read_root():
    return {"message": "Welcome to the Robo Advisor API!"}

@app.get("/advice")
def get_investment_advice(date: str = Query(..., description="Date in YYYY-MM-DD format")):
    try:
        start_date = datetime.strptime(date, "%Y-%m-%d")
        end_date = start_date + timedelta(days=1)
        date_list = [start_date.strftime("%Y-%m-%d")]

        news_downloader = Finnhub_Date_Range({"token": FINNHUBAPI_KEY})
        news_downloader.download_date_range_stock(start_date=start_date, end_date=end_date, stock=STOCK)
        news = news_downloader.dataframe
        news["date"] = news.datetime.dt.date
        news["date"] = news["date"].astype("str")
        news = news.sort_values("datetime")

        respond_list = []
        headline_list = []
        summary_list = []

        for date in date_list:
            today_news = news[news.date == date]
            headlines = today_news.headline.tolist()
            headlines = "\n".join(headlines)
            headline_list.append(headlines)
            news_urls = today_news.url.tolist()

            summary = today_news.summary.tolist()
            summary = "\n".join(summary)
            summary_list.append(summary)

            prompt = f"There are news about {COMPANY_NAME}, with the stock code '{STOCK}' on {date}. The news headlines are:\n{headlines}. Here is the summary of the news:\n\n{summary}\n\nPlease provide a brief summary of these news and analyze the potential trend in the stock price for {COMPANY_NAME}. Include detailed trend results based on various assumptions."

            Robo_advisor = Openai_Chat_Agent(chat_agent_args)
            res = Robo_advisor.get_single_response(prompt)
            respond_list.append(res)
            time.sleep(3)

        investment_advice = respond_list[0]
        return {"investment_advice": investment_advice}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
