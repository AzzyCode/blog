from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
from openai import OpenAI
import random
import os

from nicegui import ui

load_dotenv()

client = OpenAI(
    base_url = "https://openrouter.ai/api/v1",
    api_key = os.getenv("OPENROUTER_API_KEY"),
)


app = FastAPI()


def generate_random_article():
    titles = ["The Future of AI", "Python Tips and Tricks", "Web Development Trends", "Random Thoughts"]
    contents = [
        "Artifical intelligence is transforming the world...",
        "Here are some Python tips to improve your code...",
        "Web development is evolvign rapidly with new frameworks...",
        "Sometimes, randomness leads to the best ideas..."
    ]
    return {
        "title": random.choice(titles),
        "content": random.choice(contents)
    }
    

async def fetch_fun_fact():
    """Fetch a fun fact using DeepSeek model."""
    try:
        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "<YOUR_SITE_URL>",
                "X-Title": "<YOUR_SITE_NAME>", 
            },
            model = "deepseek/deepseek-r1:free",
            messages = [
                {
                    "role": "user",
                    "content": "Tell me a fun fact."
                }
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error fetching fun fact: {str(e)}"


@ui.page("/")
def index():
    """Home page UI."""
    with ui.column().classes("w-full items-center"):
        ui.label("Welcome to my Blog!").classes("text-h3 font-bold text-blue-600")
        ui.button("Generate random article", on_click=lambda: ui.navigate.to("/random-article"))
        ui.button("Get a Fun Fact!", on_click=lambda: ui.navigate.to("/fun-fact"))


# Random article page
@ui.page("/random-article")
def random_article():
    article = generate_random_article()
    ui.label(article["title"]).classes("text-h2")
    ui.markdown(article["content"])
    ui.button("Back to Home", on_click=lambda: ui.navigate.to("/"))
    

@ui.page("/fun-fact")
async def fun_fact():
    """Page to display a fun fact using DeepSeek model."""
    fact = await fetch_fun_fact()
    with ui.column().classes("w-full items-center"):
        ui.label("Random Fun Fact").classes("text-h2 font-bold text-purple-600")
        ui.markdown(fact).classes("text-lg")
        ui.button("New fun fuct", on_click=lambda: ui.navigate.to("/fun-fact"))
        ui.button("Back to Home", on_click=lambda: ui.navigate.to("/"))
    
    
ui.run_with(app)



