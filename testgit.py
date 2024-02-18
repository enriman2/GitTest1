from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key = os.environ["APIKEY"])

#Put your story here
story = "Her husband was a magician that was doing a gun trick with an apple on her head and his eyes closed. He didn't realize that she was wearing high heals so he didn't calculate the height accurately.... so he killed her."

conversation = [
    {"role": "system", "content": "You are going to help the player guess the entierety of the story and you are designed to output JSON"},
    {"role": "system", "content": "This is a story: " + story},
    {"role": "system", "content": "The player is going to ask a yes/no question about the story, and you must answer this way: you reason your answer, and then you say Yes or No."},
    {"role": "system", "content": "If the story is that someone killed his cat, then if the question is 'Did a human die?', your answer should be: {'reasoning': 'Someone killed his cat, so no human died in this story', 'relevance': True, 'yes_or_no_question': True, 'answer': 'No'}. If the question is 'Did the cat die?', then your answer should be: {'reasoning': 'Someone killed his cat, so the cat died', 'relevance': True, 'yes_or_no_question': True, 'answer': 'Yes'}. If the question is 'Did the cat kill the human?', your answer should be: {'reasoning': 'Someone killed his cat, so the cat didn't kill the human', 'relevance': True, 'yes_or_no_question': True, 'answer': 'No'}."}
]

while True:
    conversation.append({"role": "user", "content": input()})
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        response_format={ "type": "json_object" },
        messages=conversation
    )
    print(response.choices[0].message.content)
    conversation.append({"role": "assistant", "content": response.choices[0].message.content})
