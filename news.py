import requests
from openai import OpenAI

from config import NEWS_API_KEY
from config import OPENAI_API_KEY
from config import NEWS_COUNT
from config import LANGUAGE

client = OpenAI(api_key=OPENAI_API_KEY)


def get_news(topic):

    url = "https://www.thenewsapi.com/account/dashboard"

    params = {
        "q": topic,
        "language": LANGUAGE,
        "sortBy": "publishedAt",
        "pageSize": NEWS_COUNT,
        "apiKey": NEWS_API_KEY
    }

    try:

        response = requests.get(url, params=params)

        data = response.json()

        return data.get("articles", [])

    except Exception as e:

        print("News error:", e)

        return []


def summarize(text):

    try:

        response = client.chat.completions.create(

            model="gpt-4.1-mini",

            messages=[
                {
                    "role": "user",
                    "content": f"Summarize this news in 2 short sentences:\n{text}"
                }
            ]

        )

        return response.choices[0].message.content

    except Exception as e:

        print("Summary error:", e)

        return "Summary not available."
