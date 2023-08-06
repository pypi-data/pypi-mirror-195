import unittest

from mlops_models.sentiment import TweetSentiment


class TestTweetSentiment(unittest.TestCase):

	def test_positive(self):

		model = TweetSentiment()
		self.assertEqual(model.predict("Amazing, I love this"), 1)


	def test_negative(self):

		model = TweetSentiment()
		self.assertEqual(model.predict("This is chaos"), -1)

		self.assertEqual(model.predict("Amazing, this is crazy"), -1)


	def test_neutral(self):

		model = TweetSentiment()
		self.assertEqual(model.predict("what about that"), 0)



	# test data cleaning function
	def test_data_cleaning(self):

		# test special characters removed
		model = TweetSentiment()
		self.assertEqual(model._data_cleaning_("Amazing, I love this!"), "amazing i love this")





## To run the tests
# bash
# python -m unittest discover -s src/tests -p "test_*.py"