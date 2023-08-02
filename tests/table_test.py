
import sys, os
sys.path.append(os.path.join(sys.path[0],'table_processing'))

def test_data_frame_exists():
    from huggingface_hub import hf_hub_download
    from PIL import Image
    import pandas as pd
    from table_processing.Table import Table

    file_path = hf_hub_download(repo_id="nielsr/example-pdf", repo_type="dataset", filename="example_table.png")
    table_image = Image.open(file_path).convert("RGB")
    width, height = table_image.size
    table_image.resize((int(width*0.5), int(height*0.5)))
    table = Table(image = table_image)
    assert type(table.get_as_dataframe()) == type(pd.DataFrame())


def test_to_excel():
    from table_processing.Table_Detector import Table_Detector
    import os
    if os.path.exists("demofile.txt"):
        os.remove("all_excel.xlsx")

    table_detector = Table_Detector(file = "resources/multipletab.pdf")
    table_detector.to_excel()
    assert os.path.exists("all_excel.xlsx")
    os.remove("all_excel.xlsx")
    assert not os.path.exists("all_excel.xlsx")

def test_calculate_row_column_limits():
    # TODO: Make a test for calculate_row_column_limits
    assert False

def test_get_cropped_rows():
    # TODO: Make a test case for get_cropped_rows
    assert False

def test_get_cropped_columns():
    # TODO: Make a test case for get_cropped_columns
    assert False

def test_extract_table_content():
    import pandas as pd
    from table_processing.Table import Table
    from table_processing.Table_Detector import Table_Detector
    from table_processing.table_metrics import test_tables

    t_name = 'MknamLBhTbMkiPABhMhN5V'
    file_path = './tests/resources/' + t_name + '/'  + t_name
    trueT = pd.read_excel(file_path+'_true.xlsx')
    detc_table = Table_Detector(file_path+'.pdf')
    table = detc_table.get_page_data()[0]['tables'][0]['table_content']
    readT = Table.get_as_dataframe(table)
    metrics_df = test_tables({t_name: [trueT,readT]})

    assert metrics_df['Overlap'][t_name] >= 0.8
    assert metrics_df['String Similarity'][t_name] >= 0.75
    assert metrics_df['Completeness'][t_name] >= 0.6
    assert metrics_df['Purity'][t_name] >= 0.6
    assert metrics_df['Precision'][t_name] >= 0.5
    assert metrics_df['Recall'][t_name] >= 0.5


def test_remove_duplicate_limits():
    from table_processing.table_tools import remove_duplicate_limits
    limit_list = [0, 0.1, 0.1, 50, 60, 0, 51, 52, -50]
    threshold = 2
    unique = remove_duplicate_limits(limit_list, threshold)
    expected = [-50, 0, 50, 52, 60]
    expected.sort()
    unique.sort()
    assert expected == unique


def test_within_threshold():
    from table_processing.table_tools import within_threshold
    assert within_threshold(1, 1, 1) == True
    assert within_threshold(1, 5, 1) == False
    assert within_threshold(1.3, 1.4, 1) == True
    assert within_threshold(1.3, 1.4, 0.01) == False
