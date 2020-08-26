import csv


class CsvCacher:
    """Class that handles a cache and writes it to a file"""

    def __init__(self, filename='cache.csv'):
        """Constructor

        Parameters:
            filename (str): The csv file where the cache will be stored
        """
        self._cache = []
        self._filename = filename

    def add_to_cache(self, question, answer):
        """
        Add a question and its answer to the cache

        Parameters:
            question (str): The question
            answer (str): The answer to the question
        """
        if not isinstance(question, str) or not isinstance(answer, str):
            return
        if question and answer:
            self._cache.append((question, answer))

    def write_cache(self):
        """Write cache to file"""
        with open(self._filename, 'w') as cache_file:
            writer = csv.writer(cache_file, delimiter=',')
            writer.writerow(['Question', 'Answer'])
            for cached_element in self._cache:
                writer.writerow(cached_element)
