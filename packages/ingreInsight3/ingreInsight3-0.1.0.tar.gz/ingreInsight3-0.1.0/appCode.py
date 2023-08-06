from __future__ import print_function
from pyzbar.pyzbar import decode
import openai
import openfoodfacts
from tenacity import retry, wait_random_exponential

openai.api_key = "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"

# Makes sure ChatGPT doesn't go off course
messages = [
    {"role": "system", "content": "You are a kind helpful assistant."},
]

# Keeps prompting ChatGPT incase the rate limit has been reached
@retry(wait=wait_random_exponential(min=1, max=60))
def completion_with_backoff(**kwargs):
        return openai.ChatCompletion.create(**kwargs)

def chatGPT(message):
    # Asking ChatGPT about ingredient
    messages.append({"role": "user", "content": message},)
    chat = completion_with_backoff(model="gpt-3.5-turbo", messages=messages)
    return chat.choices[0].message.content

# Scans barcode and finds ingredients
def scan(frame):
    ingreList = []
    code = decode(frame)
    if len(code) > 0:
        # Obtains and displays ingredients using barcode
        product = openfoodfacts.products.get_product(code[0][0].decode())
        if product.get('product') != None:
            for ingredients in product['product']['ingredients_hierarchy']:
                ingredient = ingredients.replace("en:", "")
                ingredient = ingredient.replace("-", " ")
                ingreList.append(ingredient)
            return (ingreList)

# Information on ingredients
def info(i):
    summ = chatGPT(f"What is {i} in simple terms?")
    # Makes sure the answer is only a number
    answer = chatGPT(f"On a scale from 1 to 5, 1 being unhealthy and 5 being healthy, how healthy is {i}? Only reply with a number.")
    num = [x for x in answer.split() if x.isdigit()] 
    # NOTES: Make it only display the countries
    coun = chatGPT(f"Is {i} banned in any countries?")
    # NOTES: Make it only tell which allergies
    aller = chatGPT(f"Does {i} affect any allergies?")
    return (summ, num, coun, aller)