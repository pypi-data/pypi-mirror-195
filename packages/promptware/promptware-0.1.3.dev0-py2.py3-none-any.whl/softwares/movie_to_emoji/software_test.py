import os
import sys
import unittest

current_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(current_path)

from .software import MovieToEmojiPromptware  # noqa


class TestMovieToEmojiPromptware(unittest.TestCase):
    def test_write_to_directory(self):
        software = MovieToEmojiPromptware()
        file_path = software.info.write_to_directory(current_path)
        self.assertTrue(os.path.exists(file_path))

    # def test_execute(self):
    #     software =MovieToEmojiPromptware()

    #     input={"text": "Star Wars:"}
    #     result = software.execute(input)
    #     print(result)
