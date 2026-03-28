import telebot

from config import TOKEN
from config import DEFAULT_TOPIC

from news import get_news
from news import summarize

bot = telebot.TeleBot(TOKEN)

# хранение тем пользователей

user_topics = {}


@bot.message_handler(commands=["start"])
def start(message):

    chat_id = message.chat.id

    user_topics[chat_id] = DEFAULT_TOPIC

    bot.send_message(

        chat_id,

        "Welcome!\n\n"
        "Write a topic.\n\n"
        "Examples:\n"
        "gaming\n"
        "AI\n"
        "crypto\n"
        "technology"

    )


@bot.message_handler(commands=["news"])
def manual_news(message):

    send_news(message.chat.id)


@bot.message_handler(func=lambda m: True)
def set_topic(message):

    chat_id = message.chat.id

    topic = message.text

    user_topics[chat_id] = topic

    bot.send_message(

        chat_id,

        f"Topic set: {topic}\nGetting news..."

    )

    send_news(chat_id)


def send_news(chat_id):

    topic = user_topics.get(chat_id, DEFAULT_TOPIC)

    articles = get_news(topic)

    if not articles:

        bot.send_message(

            chat_id,

            "No news found."

        )

        return

    for article in articles:

        title = article.get("title", "")

        description = article.get("description", "")

        url = article.get("url", "")

        text = title + " " + description

        summary = summarize(text)

        message = (

            f"📰 {title}\n\n"
            f"{summary}\n\n"
            f"{url}"

        )

        bot.send_message(chat_id, message)


print("Bot started")

bot.infinity_polling()
