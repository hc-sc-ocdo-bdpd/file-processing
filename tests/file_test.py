import sys, os
sys.path.append(os.path.join(sys.path[0],'file_processing'))

def test_txt_text():
    from file_processing.file import File
    txt_1 = File('tests/resources/test_files/government_of_canada_wikipedia.txt')
    txt_2 = File('tests/resources/test_files/usa_government_wikipedia.txt')
    assert len(txt_1.metadata['text']) == 38983
    assert len(txt_2.metadata['text']) == 47819

def test_txt_num_lines():
    # indirectly tests lines attribute
    from file_processing.file import File
    txt_1 = File('tests/resources/test_files/government_of_canada_wikipedia.txt')
    txt_2 = File('tests/resources/test_files/usa_government_wikipedia.txt')
    assert txt_1.metadata['num_lines'] == 306
    assert txt_2.metadata['num_lines'] == 383

def test_txt_num_words():
    # indirectly tests words attribute
    from file_processing.file import File
    txt_1 = File('tests/resources/test_files/government_of_canada_wikipedia.txt')
    txt_2 = File('tests/resources/test_files/usa_government_wikipedia.txt')
    assert txt_1.metadata['num_words'] == 5691
    assert txt_2.metadata['num_words'] == 7160