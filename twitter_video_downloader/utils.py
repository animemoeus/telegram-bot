import urllib

import requests
from bs4 import BeautifulSoup
from django.utils.encoding import iri_to_uri, uri_to_iri


def ssstwitter_com(tweet_url: str):
    url = "https://ssstwitter.com/"

    payload = f"id={urllib.parse.quote_plus(tweet_url)}&locale=en&tt=60235e3409bd9bbf594d18d0ae0636ac&ts=1693738774&source=form"
    headers = {
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "hx-current-url": "https://ssstwitter.com/",
        "hx-request": "true",
        "hx-target": "target",
        "origin": "https://ssstwitter.com",
        "pragma": "no-cache",
        "referer": "https://ssstwitter.com/",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if not response.status_code == 200:
        return {"status": response.status_code, "data": {}, "message": ""}

    html_doc = response.text
    soup = BeautifulSoup(html_doc, "html.parser")
    arter = soup.find("div", {"class": "result_overlay"}).find_all("a")

    tweet_data = []
    for i in arter[:-1]:
        tweet_data.append({"text": " ".join(i.text.split()), "url": i.get("href")})

    return {
        "status": response.status_code,
        "data": tweet_data,
        "message": "https://ssstwitter.com/",
    }
