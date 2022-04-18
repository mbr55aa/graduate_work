"""Класс классификатор зпросов."""
import logging

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC

logger = logging.getLogger(__name__)


class Classifier:
    """Класс классификатор зпросов для угадывания намерений пользователя."""

    def __init__(self, commands: dict):
        """
        Функция инициализации экземпляра класса.
        :param config: Словарь с возможными командами.
        """
        self.commands = commands
        self.vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(2, 3))
        self.classifier_probability = LogisticRegression()
        self.classifier = LinearSVC()
        self.prepare_corpus()

    def prepare_corpus(self):
        """
        Подготовка модели для угадывания намерения пользователя.
        """
        corpus = []
        target_vector = []
        for intent_name, intent_data in self.commands['intents'].items():
            for example in intent_data['examples']:
                corpus.append(example)
                target_vector.append(intent_name)

        training_vector = self.vectorizer.fit_transform(corpus)
        self.classifier_probability.fit(training_vector, target_vector)
        self.classifier.fit(training_vector, target_vector)

    def get_intent(self, request: str) -> str:
        """
        Получение наиболее вероятного намерения в зависимости от запроса пользователя
        :param request: запрос пользователя (первая часть запроса)
        :return: наиболее вероятное намерение
        """
        best_intent = self.classifier.predict(self.vectorizer.transform([request]))[0]

        index_of_best_intent = list(self.classifier_probability.classes_).index(best_intent)
        probabilities = self.classifier_probability.predict_proba(self.vectorizer.transform([request]))[0]

        best_intent_probability = probabilities[index_of_best_intent]
        logger.info(f'{request}:{best_intent_probability}')
        # при добавлении новых намерений стоит уменьшать этот показатель
        if best_intent_probability > 0.282:
            logger.info(f'Выбрал {best_intent}')
            return best_intent
        # return best_intent_probability
