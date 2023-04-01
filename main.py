import requests
from itertools import islice
from newsapi import NewsApiClient
import smtplib


def take(n, iterable):
    return list(islice(iterable, n))

def send_email():
    with smtplib.SMTP('smtp.gmail.com', port=587) as connection:
    connection.starttls()
    connection.login(user=my_email, password=password)
    connection.sendmail(from_addr=my_email, to_addrs='email@gmail.com', msg=f"Bitcoin price alert:\nBTC price has changed by {price_change}!\nThe top headline for this is:\n {top_headline}")

    
my_email = 'MY_EMAIL'
password = 'MY_PASSWORD'
STOCK_ENDPOINT = "https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol=BTC&market=CNY&apikey=Z803QX8XL03OEVJF"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
news_api_key = 'NEWS_API_KEY'


stock_client = requests.get(STOCK_ENDPOINT)
btc_price = take(2, stock_client.json()["Time Series (Digital Currency Daily)"].items())
btc_one_day_close = float(btc_price[0][1]["4b. close (USD)"])
btc_two_day_close = float(btc_price[1][1]["4b. close (USD)"])

news_api = NewsApiClient(api_key=news_api_key)
try:
    top_headline = news_api.get_top_headlines(q="bitcoin")['articles'][0]['title']
except IndexError:
    top_headline = "No headlines found today!"

price_change = ((btc_one_day_close - btc_two_day_close) / btc_two_day_close) * 100
if price_change > 5:
    send_email()
