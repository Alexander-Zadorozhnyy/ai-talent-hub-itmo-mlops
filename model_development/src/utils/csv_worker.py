import csv


class CSVWorker:
    @staticmethod
    def write(path, samples):
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["text", "label"])
            writer.writeheader()
            for sample in samples:
                writer.writerow({"text": sample[0], "label": sample[1]})

    @staticmethod
    def load(path):
        texts, labels = [], []
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                texts.append(row["text"])
                labels.append(row["label"])
        return texts, labels
