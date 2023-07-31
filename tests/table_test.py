
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
    from table_processing.table_tools import _calculate_row_column_limits,remove_duplicate_limits
    expected_row_limit=[]
    expected_col_limit=[]
    img_dim = (730,250)
    test_bbox = [[122,122.7,133,42],[50,40,123,100],[26,107,108.2,111]]
    for box in test_bbox:
        x1,y1,x2,y2 = box
        expected_row_limit.append(y1)
        expected_row_limit.append(y2)
        expected_col_limit.append(x1)
        expected_col_limit.append(x2)
    
    expected_col_limit.sort()
    expected_row_limit.sort()

    expected_col_limit = remove_duplicate_limits(expected_col_limit,4)
    expected_row_limit = remove_duplicate_limits(expected_row_limit,4)

    expected_col_limit.pop(0)
    expected_col_limit.pop()


    expected_col_limit.append(0)
    expected_col_limit.append(img_dim[0])
    expected_row_limit.append(0)
    expected_row_limit.append(img_dim[1])

    expected_col_limit.sort()
    expected_row_limit.sort()

    returned_col_limit, returned_row_limit = _calculate_row_column_limits(img_dim,test_bbox)


    assert expected_col_limit == returned_col_limit and expected_row_limit == returned_row_limit

    

    # TODO: Make a test for calculate_row_column_limits

def test_get_cropped_rows():
    # TODO: Make a test case for get_cropped_rows
    assert False

def test_get_cropped_columns():
    # TODO: Make a test case for get_cropped_columns
    assert False

def test_extract_table_content():
    from PIL import Image
    import pandas as pd
    from table_processing.Table import Table

    file_path = "./tests/resources/simple_table.PNG"
    table_image = Image.open(file_path).convert("RGB")
    width, height = table_image.size
    table_image.resize((int(width*0.5), int(height*0.5)))
    table = Table(image = table_image)

    # TODO: Correct this test case to check the table contents
    assert False


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
