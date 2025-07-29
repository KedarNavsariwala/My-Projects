import os
import requests
import json
import subprocess
from typing import List
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from IPython.display import Markdown, display, update_display
from openai import OpenAI

def age_define():
    
    age = int(input("Enter your Age: "))

    if age >= 18:
        print("You are an adult.")
    else:
        print("You are a minor.")

def simpleloop():

    i = int(input("Enter a number: "))

    for i in range(5):
        print(i)

def stringcounter(S, s):
    
    return S.count(s)

def prompt(x):

    try:
        result = subprocess.run(
            ["ollama", "run", "llama3.2", x],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",  # Add this line
            shell=True  # For compatibility with PowerShell/Terminal
        )
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error running ollama: {e.stderr}")

condition = 'yes'

while condition == 'yes':
    x = input("Enter your prompt: ")
    prompt(x)
    condition = input("Do you want to continue? (yes/no): ").strip().lower()
    if condition == 'no':
        print("Exiting the loop.")
        break
    else:
        print("Please enter next question.")
        continue

