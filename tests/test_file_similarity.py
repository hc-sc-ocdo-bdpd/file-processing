import pytest
from file_processing import File
from file_processing import CosineSimilarity
from file_processing import LevenshteinDistance

variable_names = "a, b, cosine, levenshtein"
values = [("tests/resources/similarity_test_files/aviation_safety.txt",
           "tests/resources/similarity_test_files/express_entry.txt",
           0.27, 2816),

          ("tests/resources/test_files/ArtificialNeuralNetworksForBeginners.pdf",
           "tests/resources/test_files/SampleReport.docx",
           0.01, 13476),

          ("tests/resources/test_files/2021_Census_English.csv",
           "tests/resources/test_files/HealthCanadaOverviewFromWikipedia.pptx",
           0.06, 6082663)]


@pytest.mark.parametrize(variable_names, values)
def test_similarity_scores(a, b, cosine, levenshtein):
    file_a = File(a)
    file_b = File(b)
    cos = CosineSimilarity(file_a, file_b).calculate()
    lev = LevenshteinDistance(file_a, file_b).calculate()

    assert cosine == round(cos, 2), "Cosine similarity is wrong"
    assert levenshtein == round(lev, 2), "Levenshtein distance is wrong"
