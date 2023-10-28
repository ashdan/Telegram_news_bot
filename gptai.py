import openai
from variables import GPT_TOKEN



def get_GPT(text):
    openai.api_key = GPT_TOKEN
    response = openai.ChatCompletion.create(
    model="gpt-4",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": "Как администратор новостного канала напиши короткое изложение новости (не больше 100 слов)"
            },
            {
                "role": "user",
                "content": text
            }
        ])
    return response['choices'][0]['message']['content']

# def get_GPT(text):
#     return text[0:255]


