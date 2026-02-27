class NameGenerator:
    def __init__(self, source_path='nicknames.txt'):
        self.source_path = source_path
        self.names = self.fetch()

    def fetch(self):
        """
        Loads nicknames from a local curated text file (one nickname per line).
        """
        names = []
        try:
            with open(self.source_path, encoding='utf-8') as handle:
                for line in handle:
                    value = line.strip()
                    if value and not value.startswith('#'):
                        names.append(value)
        except FileNotFoundError:
            return []
        return names
