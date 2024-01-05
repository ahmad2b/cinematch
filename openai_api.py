import requests as req
import streamlit as st
import asyncio
import json
import time
from openai import OpenAI

from typing import List, Any

from openai.types.beta import Assistant
from openai.types.beta.thread import Thread
from openai.types.beta.threads.run import Run
from openai.types.beta.threads.thread_message import ThreadMessage

from tmdb_api import MovieDB


class AsyncManager:
    def __init__(self):
        self.movie_db = MovieDB()

    def run_until_complete(self, task):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(task)

    def search_movies_by_keywords(self, keywords: List[str]):
        print("search_movies_by_keywords", keywords)
        task = self.movie_db.search_movies_by_keywords(keywords)
        return self.run_until_complete(task)


class MessageItem:
    def __init__(self, role: str, content: str | Any):
        self.role: str = role
        self.content: str | Any = content


class OpenAIBot:
    def __init__(self, model: str = "gpt-3.5-turbo-1106") -> None:
        OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
        assistants_id = "asst_sA2PRCNHBFq8Ca9fVbEXllBp"

        self.model: str = model
        self.client: OpenAI = OpenAI(api_key=OPENAI_API_KEY)
        self.assistant = self.client.beta.assistants.retrieve(assistants_id)
        self.thread: Thread = self.client.beta.threads.create()
        self.messages: list[MessageItem] = []

    def send_message(self, message: str):
        print("message: ", message)
        latest_message: ThreadMessage = self.client.beta.threads.messages.create(
            thread_id=self.thread.id, role="user", content=message
        )
        print("latest_message: ", latest_message)

        self.latest_run: Run = self.client.beta.threads.runs.create(
            thread_id=self.thread.id,
            assistant_id=self.assistant.id,
        )

        # print("message sent on thread id: ", self.thread.id)
        self.addMessage(MessageItem(role="user", content=message))

    def isCompleted(self) -> bool:
        print("Status: ", self.latest_run.status)
        while self.latest_run.status != "completed":
            print("Going to sleep")
            time.sleep(1)
            self.latest_run: Run = self.client.beta.threads.runs.retrieve(  # type: ignore
                thread_id=self.thread.id, run_id=self.latest_run.id
            )
            print("Latest Status: ", self.latest_run.status)
            # print("Latest Run: ", self.latest_run)
        return True

    def get_lastest_response(self) -> MessageItem:
        messages = self.client.beta.threads.messages.list(thread_id=self.thread.id)
        print("Response: ", messages.data[0])
        m = MessageItem(messages.data[0].role, messages.data[0].content[0].text.value)
        self.addMessage(m)
        return m

    def getMessages(self) -> list[MessageItem]:
        return self.messages

    def addMessage(self, message: MessageItem) -> None:
        self.messages.append(message)
