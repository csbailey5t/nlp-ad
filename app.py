from fastapi import FastAPI
import random
import requests

app = FastAPI()

workshops_url = "https://www.lib.ncsu.edu/rest_workshops/master-workshops-feed.json"


async def get_workshop_data(url: str):
    r = requests.get(url)
    return r.json()


@app.get("/")
async def root():
    data = await get_workshop_data(workshops_url)
    random_workshop = random.choices(data, k=1)
    return {"workshops": random_workshop}