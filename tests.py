import unittest
from unittest import IsolatedAsyncioTestCase
from bot import hello


class Author:
    def __init__(self):
        self.name = "Test user"

class Message:
    def __init__(self):
        self.author = Author()

class Context:
    def __init__(self):
        self.message = Message()
    
    def send(self, message):
        return message


class Test(IsolatedAsyncioTestCase):

    async def test_functionality(self):
        ctx = Context()
        result = await hello(ctx)
        expected = "test"
        self.assertEqual(expected, result)

if __name__ == "__main__":
    unittest.main()