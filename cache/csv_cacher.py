import csv


class CsvCacher:
    def __init__(self, filename='cache.csv'):
        self.cache = []
        self.filename = filename

    def add_to_cache(self, question, answer):
        self.cache.append((question, answer))

    def write_cache(self):
        with open(self.filename, 'w') as cache_file:
            writer = csv.writer(cache_file, delimiter=',')
            writer.writerow(['Question', 'Answer'])
            for cached_element in self.cache:
                writer.writerow(cached_element)
