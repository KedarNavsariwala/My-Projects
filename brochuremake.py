import os
import requests
import json
from typing import List
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from IPython.display import Markdown, display, update_display
from openai import OpenAI
import subprocess

subprocess.run(
            ["ollama", "run", "llama3.2"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            shell=True  # For Windows compatibility
        )

openai = OpenAI(base_url='http://localhost:11434/v1', api_key='ollama')

headers = {
 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}

class Website:

    def __init__(self, url):
        """
        Create this Website object from the given url using the BeautifulSoup library
        """
        self.url = url
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.title = soup.title.string if soup.title else "No title found"
        content_area = soup.body if soup.body else soup
        for irrelevant in content_area(["script", "style", "img", "input"]):
            irrelevant.decompose()
        self.text = content_area.get_text(separator="\n", strip=True)