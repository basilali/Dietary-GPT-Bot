from openai import OpenAI
import json

with open("key.txt") as file:
    key = file.read()
client=OpenAI(api_key = key)

"""
This file implements the bot logic
Basil Ali
"""
def read_few_shots(filename):
    """
    Reads few-shot examples from a json file
    :param filename: The filename of the json file
    :return: docs: The example text, labels: the example labels
    """
    docs = []
    labels = []

    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)
        for d in data:
            docs.append(d["input"])
            labels.append(d["label"])

    return docs, labels

def build_relevance_prompt(docs, labels, instructions):
    """
    Builds the prompt used to classify text as relevant or irrelevant
    :param docs: Few-shot examples text
    :param labels: Few-shot examples labels
    :param instructions: Additional instructions to add to the prompt
    :return: The relevance prompt
    """
    relevance_prompt = instructions + "\n"
    for i in range(len(docs)):
        relevance_prompt += "Input: " + docs[i] + "\n"
        relevance_prompt += "Relevance: " + str(labels[i]) + "\n"

    return relevance_prompt

def get_relevance(relevance_prompt, utterance):
    """
    Makes an API call to get the relevance of the user's utterance
    :param relevance_prompt: The prompt used to classify text as relevant or irrelevant
    :param utterance: The user's utterance to classify
    :return: 1 (relevant) or 0 (not relevant)
    """
    relevance_prompt += "Input" + utterance + "\n"
    relevance_prompt += "Relevance: "

    response = client.completions.create(model="gpt-3.5-turbo-instruct", prompt=relevance_prompt, temperature=0,
                                         max_tokens=1)
    relevance = response.choices[0].text

    return relevance

def get_response(dialog):
    """
    Makes an API call to get the response of the user's utterance and appends it to the dialog
    :param dialog: The dialog to get the response for
    :return: The new dialog
    """
    response = client.chat.completions.create(model="gpt-4o", messages=dialog, temperature=1, max_tokens=500)
    dialog.append(response.choices[0].message)
    return dialog

def read_text_file(filename):
    """
    Reads a text file and returns the contents as a string
    :param filename: The file to read from
    :return: The contents of the file as a string
    """
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()
    return content

def main():
    few_shots_filename = "data.json"
    relevance_instructions_filename = "relevance_instructions.txt"
    assistant_instructions_filename = "assistant_instructions.txt"
    relevance_instructions = read_text_file(relevance_instructions_filename)
    assistant_instructions = read_text_file(assistant_instructions_filename)

    print(
        "I can assist you in tuning any recipe for your dietary needs! Just provide a list of ingredients and let me "
        "know what dietary restrictions you need fulfilled!"
    )

    docs, labels = read_few_shots(few_shots_filename)
    relevance_prompt = build_relevance_prompt(docs, labels, relevance_instructions)
    dialog = [
        {"role": "system", "content": assistant_instructions}
    ]

    while True:
        utterance = input(">>> ")
        relevance = get_relevance(relevance_prompt, utterance)
        if relevance == "1":
            dialog.append({ "role": "user", "content": utterance })
            dialog = get_response(dialog)
            print(dialog[len(dialog) - 1].content)
        elif relevance == "0":
            print("Sorry, I can't help you with that.")

if __name__ == "__main__":
    main()