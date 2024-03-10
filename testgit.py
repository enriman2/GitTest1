from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()
client = OpenAI(api_key = os.environ["APIKEY"])
answerai = {}

#Put your story here
shortstory = "A man lives on the 10th floor of a building. Every morning he takes the elevator to the ground floor to go to work or just go for a walk. On his return he always takes the elevator to the 7th floor and the other 3 remaining, until he reaches his apartment, he takes them up the stairs on foot. Why does he do this?"
story = "The man is a dwarf so he has no problem pressing the button for the ground floor but he does not reach the button for the 10th floor, the maximum he can reach is the button for the 7th floor."
milestones = {"The man is dwarf": False, "He doesn't reach the elevator button": False}

conversation = [
    {"role": "system", "content": "You are going to help the player guess the entierety of the story, and you are designed to output JSON"},
    {"role": "system", "content": "This is the story: " + shortstory + ". " + story},
    {"role": "system", "content": "The player is going to ask a yes/no question about the story, and you must answer this way: {'reasoning': 'a', 'relevance': 'b', 'yes_or_no_question': 'c', 'answer': 'd'}, where 'a' must be the reasoned and detailed answer to the question and you must finish your reasoning by the answer in the form of Yes or No, 'b' must be a string that indicates if the question is relevant to this story and only to this story so if they ask anything else or a question that is irrelevant 'b' should be False and if the question is relevant 'b' should be True, 'c' must be a string that indicates if the question is a yes or no question so if the question is a yes or no question 'b' should be True and if the question isn't 'b' should be False, and 'd' must be the answer to the question based on the reasoning that you did before and in a Yes or No format."},
    {"role": "system", "content": "Your answer must always always always contain ALL of these variables: reasoning, relevance, yes_or_no_question, answer. Even if the relevance is False or the yes_or_no_question is False, you must always include them in your output. Do NOT REMOVE VARIABLES FROM THE ANSWER AND DO NOT ADD MORE VARIABLES TO THE ANSWER OTHER THAN THESE"},
    {"role": "system", "content": "If the story is that someone killed his cat, then if the question is 'Did a human die?', your answer should be: {'reasoning': 'Someone killed his cat, so no human died in this story, so No', 'relevance': True, 'yes_or_no_question': True, 'answer': 'No'}. If the question is 'Did the cat die?', then your answer should be: {'reasoning': 'Someone killed his cat, so the cat died, so Yes', 'relevance': True, 'yes_or_no_question': True, 'answer': 'Yes'}. If the question is 'Did the cat kill the human?', your answer should be: {'reasoning': 'Someone killed his cat, so the cat didn't kill the human, so No', 'relevance': True, 'yes_or_no_question': True, 'answer': 'No'}."},
]
tempconversation = []

print(shortstory)
while True:
    conversation.append({"role": "user", "content": input()})
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        response_format={ "type": "json_object" },
        messages=conversation
    )
    answerai = json.loads(response.choices[0].message.content)
    #print(answerai)
    if(answerai["relevance"] is False):
        print("Your question is not relevant to the story")
        conversation.append({"role": "assistant", "content": "Your question is not relevant to the story"})
    elif(answerai["yes_or_no_question"] is False):
        print("Please ask a yes or no question")
        conversation.append({"role": "assistant", "content": "Please ask a yes or no question"})
    else:
        print(answerai["answer"])
        conversation.append({"role": "assistant", "content": response.choices[0].message.content})
        tempconversation = conversation
        tempconversation.append({"role": "system", "content": "I am going to give you a dictionnary of milestones that the player must discover to win the game. You are going to check each milestone, and are going to see if your last answer answers to any of these milestones. You must answer in the exact same format as the milestones dictionnary, and you can only modify the value of each milestone to set it from False to True if that milestone has been discovered by the player. Here is the dictionnary of milestones: " + json.dumps(milestones)})
        tempconversation.append({"role": "system", "content": "For example, if you answered: 'Yes' to the question"})
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            response_format={ "type": "json_object" },
            messages=tempconversation
        )
        print(response.choices[0].message.content)

#ponerle ejemplos para los milestones y hacer q se edite el diccionario despues de su repuesta y verificar si todos en diccionario son true para ver si el player ha ganado
