import unittest

from mlops_models.sentiment import TweetSentiment


class TestTweetSentiment(unittest.TestCase):

	def test_positive(self):

		model = TweetSentiment()
		self.assertEqual(model.predict("Amazing, I love this"), 1)


	def test_negative(self):

		model = TweetSentiment()
		self.assertEqual(model.predict("This is chaos"), -1)


	def test_neutral(self):

		model = TweetSentiment()
		self.assertEqual(model.predict("what about that"), 0)


	# test internal model for data cleaning that returns lower case text
	def test_data_cleaning(self):
		# Test that the data cleaning function removes punctuation
		model = TweetSentiment()
		self.assertEqual(model._data_cleaning_("This is a test!"), "this is a test")

		# Test numbers
		self.assertEqual(model._data_cleaning_("This is a test 123"), "this is a test ")

		# Test upper case
		self.assertEqual(model._data_cleaning_("THIS IS A TEST"), "this is a test")

		# Test mixed case
		self.assertEqual(model._data_cleaning_("ThIs Is A tEsT"), "this is a test")

		# Test comma and period
		self.assertEqual(model._data_cleaning_("This is a test, this is a test."), "this is a test this is a test")






## To run the tests
# bash
# python -m unittest discover -s src/tests -p "test_*.py"