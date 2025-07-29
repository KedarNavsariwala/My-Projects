import os
import requests
import json
import subprocess
from typing import List
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from IPython.display import Markdown, display, update_display
from openai import OpenAI

def get_cleaned_webpage_text():
    url = input("Enter the webpage URL: ")
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Remove script and style elements
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        # Extract visible text
        text = soup.get_text(separator=' ', strip=True)
        # Collapse multiple spaces
        cleaned_text = ' '.join(text.split())
        return cleaned_text
    except Exception as e:
        print(f"Error fetching or processing the webpage: {e}")
        return ""

# Example usage:
# webpage_text = get_cleaned_webpage_text()

def summarize(x):
    try:
        result = subprocess.run(
            ["ollama", "run", "llama3.2", "Summarize the following text:", x],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",  # Add this line
            shell=True  # For compatibility with PowerShell/Terminal
        )
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error running ollama: {e.stderr}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Example usage:
# summarize()
# cleantext = get_cleaned_webpage_text()
# summarize(cleantext)

