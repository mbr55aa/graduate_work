"""
    Вспомогательный скрипт для выовода вероятностей команд
    Используется при оценке порогового значения, в случае добавления новых команд
"""
import logging
from logging import config as logger_conf

from assistant.commands import config
from classifier.classifier import Classifier
from core.log_config import LOGGING

logger_conf.dictConfig(LOGGING)
logger = logging.getLogger(__name__)
classifier = Classifier(config)

probabilities = []

for intent in config['intents']:
    for command in config['intents'][f'{intent}']['examples']:
        probability = classifier.get_intent(command)
        if probability:
            probabilities.append(probability)

logger.info(min(probabilities))
