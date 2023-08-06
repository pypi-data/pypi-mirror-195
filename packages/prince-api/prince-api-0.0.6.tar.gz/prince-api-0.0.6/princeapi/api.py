import requests


def anime_logo(text):
    API = f"https://api.princexd.tech/anime-logo?text={text}"
    req = requests.get(API).json()["url"]
    return(req)

def write(text):
    API = f"https://api.princexd.tech/write?text={text}"
    req = requests.get(API).json()["url"]
    return(req)
