## Celery task that accepts an input file as an argument, classifies sentiment of each tweet in the file, and writes the results to an output file

import os
import json
from celery import Celery
from celery.utils.log import get_task_logger
from celery.signals import worker_process_init

from mlops_models.sentiment import TweetSentiment

# Instantiate Celery application
celery = Celery()
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")

# Instantiate logger
logger = get_task_logger(__name__)

# Load model
model = TweetSentiment()

@celery.task(name="batch.process")
def process(input_file: str, output_file: str):
    """
    Celery task that accepts an input file as an argument, classifies sentiment of each tweet in the file,
    and writes the results to an output file
    :param input_file: Input file path
    :param output_file: Output file path
    :return: None
    """

    with open(input_file, 'r') as f:
        input_lines = f.read().splitlines()

    data = []
    for tweet in input_lines:
        data.append(
            {
                "text": tweet,
                "sentiment": model.predict(tweet)
            }
        )

    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)


@celery.task(name="classify")
def classify(text: str) -> int:
    """
    Celery task that classifies the sentiment of a tweet and saves results to a file
    :param text: The text of the tweet.
    :return: the path to the file containing the results
    """

    # Classify sentiment
    sentiment = model.predict(text)

    # Save results to a file
    output_file = f"{text[:10]}.json"
    with open(output_file, 'w') as f:
        json.dump(
            {
                "text": text,
                "sentiment": sentiment
            },
            f,
            indent=2
        )

    return output_file



@worker_process_init.connect
def configure_worker(**kwargs):
    """
    Celery signal that is called when a worker process is initialized.
    :param kwargs:
    :return:
    """
    global model
    model = TweetSentiment()




## To run celery worker
# celery -A src.streaming.celery worker --loglevel=info


## To class a task in shell
# from src.streaming.celery import classify
# classify.delay("I love this movie!")