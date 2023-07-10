from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .file_metric_strategy import FileMetricStrategy

class CosineSimilarity(FileMetricStrategy):
    def calculate(self):
        text1 = self.file1.metadata['text']
        text2 = self.file2.metadata['text']

        vectorizer = TfidfVectorizer().fit([text1, text2])
        tfidf_matrix = vectorizer.transform([text1, text2])

        cos_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])

        return cos_sim[0][0]
