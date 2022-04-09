"""Класс классификатор зпросов."""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC


class Classifier:
    """Класс классификатор зпросов для угадывания намерений пользователя"""

    def __init__(self, config: dict):
        self.config = config
        self.vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(2, 3))
        self.classifier_probability = LogisticRegression()
        self.classifier = LinearSVC()
        self.prepare_corpus()

    def prepare_corpus(self):
        """
        Подготовка модели для угадывания намерения пользователя
        """
        corpus = []
        target_vector = []
        for intent_name, intent_data in self.config['intents'].items():
            for example in intent_data['examples']:
                corpus.append(example)
                target_vector.append(intent_name)

        training_vector = self.vectorizer.fit_transform(corpus)
        self.classifier_probability.fit(training_vector, target_vector)
        self.classifier.fit(training_vector, target_vector)

    def get_intent(self, request: str) -> str:
        """
        Получение наиболее вероятного намерения в зависимости от запроса пользователя
        :param request: запрос пользователя
        :return: наиболее вероятное намерение
        """
        # Временно сделал проверку на полное совпадение начала запроса
        for intent in self.config['intents']:
            if request in self.config['intents'][intent]['examples']:
                return intent

        # Пока убрал, потому что работает плохо
        # best_intent = self.classifier.predict(self.vectorizer.transform([request]))[0]
        #
        # index_of_best_intent = list(self.classifier_probability.classes_).index(best_intent)
        # probabilities = self.classifier_probability.predict_proba(self.vectorizer.transform([request]))[0]
        #
        # best_intent_probability = probabilities[index_of_best_intent]
        # # при добавлении новых намерений стоит уменьшать этот показатель
        # if best_intent_probability > 0.4:
        #     return best_intent
