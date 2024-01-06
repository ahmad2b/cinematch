import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from openai_api import AsyncManager, OpenAIBot, MessageItem


def test_async_manager():
    async_manager = AsyncManager()
    assert async_manager is not None


def test_openai_bot():
    bot = OpenAIBot()
    bot.send_message("Hello, world!")
    assert bot.isCompleted()
    assert isinstance(bot.get_lastest_response(), MessageItem)
    assert len(bot.getMessages()) > 0
