from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key = os.environ["APIKEY"])

conversation = [{"role": "system", "content": "This is a story: thee are two people on a submarine, and the submarine is going to sink, so they are going to drown soon, but there is a gun with 1 bullet left, so they played a chess game, and the one who wins gets to suicide. So they play the game, one of them wins, and he shoots himself, commiting suicide, so he doesn't drown, he commits suicide. The other one drowns and dies too."},{"role": "system", "content": "The player is going to ask a yes/no question about the story, and you must reason your answer and justify it and then answer Yes or No"}]

while True:
    conversation.append({"role": "user", "content": input()})
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=conversation
    )
    print(response.choices[0].message.content)
    conversation.append({"role": "assistant", "content": response.choices[0].message.content})
