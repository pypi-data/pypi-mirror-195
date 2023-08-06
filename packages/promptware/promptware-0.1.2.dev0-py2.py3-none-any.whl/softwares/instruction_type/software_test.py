import os
import sys
import unittest

current_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(current_path)

from .software import InstructionTypePromptware  # noqa


class TestInstructionTypePromptware(unittest.TestCase):
    def test_write_to_directory(self):
        software = InstructionTypePromptware()
        file_path = software.info.write_to_directory(current_path)
        self.assertTrue(os.path.exists(file_path))
