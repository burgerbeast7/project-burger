import unittest
from app.bot import process_user_input, generate_response

class TestBot(unittest.TestCase):

    def test_process_user_input(self):
        self.assertEqual(process_user_input("Hello"), "Hi there!")
        self.assertEqual(process_user_input("What can you do?"), "I can help you order burgers!")

    def test_generate_response(self):
        self.assertEqual(generate_response("Order a burger"), "Your burger order has been placed!")
        self.assertEqual(generate_response("Cancel my order"), "Your order has been canceled!") 

if __name__ == '__main__':
    unittest.main()