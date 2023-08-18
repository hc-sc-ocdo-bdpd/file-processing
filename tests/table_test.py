
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

    table_detector = Table_Detector(filename = "resources/multipletab.pdf")
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

    expected_col_limit = remove_duplicate_limits(expected_col_limit,16)
    expected_row_limit = remove_duplicate_limits(expected_row_limit,8)

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
    from PIL import Image
    from table_processing.Table import get_cropped_rows

    #Creating image
    row_height = 30
    row_width = 234
    im_red = Image.new('RGB', size = (row_width, row_height), color=(255,0,0))
    im_green = Image.new('RGB', size = (row_width, row_height), color=(0,255,128))
    im_blue = Image.new('RGB', size = (row_width, row_height), color=(0,128,255))
    im = Image.new('RGB', size=(im_red.width, im_red.height + im_green.height + im_blue.height))
    im.paste(im_red, (0,0))
    im.paste(im_green, (0,im_red.height))
    im.paste(im_blue, (0,im_red.height + im_green.height))
    
    #Creating Ditionary holding color and size of each row in image
    color_dict = {(255,0,0): (row_width, row_height), (0,255,128): (row_width, row_height), (0,128,255): (row_width, row_height)}
    dict_items_lst = []
    for item in color_dict.items():
        dict_items_lst.append(item)
    
    #Testing part
    row_limits = [30,60,90]
    row_list = get_cropped_rows(im, row_limits)
    expected_len = len(row_limits)
    assert  expected_len == len(row_list)
    counter = 0
    for row in row_list:
        #Test right dimensions
        if counter > 0:
            assert row.size[1] == round(row_limits[counter] - row_limits[counter-1])
        else:
            assert row.size[1] == round(row_limits[counter])
        #Test right color and pixel match
        assert row_list[counter].getcolors()[0][1] == dict_items_lst[counter][0]
        assert row_list[counter].size == dict_items_lst[counter][1] 
        assert len(row_list[counter].getcolors()) == 1
        assert row_list[counter].getcolors()[0][0] == row.size[0]*row.size[1]
        counter+=1

def test_get_cropped_columns():
    from PIL import Image
    from table_processing.Table import get_cropped_columns
    
    #Creating image
    column_height = 30
    column_width = 200
    im_red = Image.new('RGB', size = (column_width, column_height), color=(255,145,35))
    im_green = Image.new('RGB', size = (column_width, column_height), color=(125,255,138))
    im_blue = Image.new('RGB', size = (column_width, column_height), color=(120,150,255))
    im = Image.new('RGB', size=(im_red.width + im_green.width + im_blue.width, column_height))
    im.paste(im_red, (0,0))
    im.paste(im_green, (im_red.width,0))
    im.paste(im_blue, (im_red.width + im_green.width, 0))
    
    #Creating Ditionary holding color and size of each column in image
    color_dict = {(255,145,35): (column_width, column_height), (125,255,138): (column_width, column_height), (120,150,255): (column_width, column_height)}
    dict_items_lst = []
    for item in color_dict.items():
        dict_items_lst.append(item)
    
    #Testing part
    column_limits = [200,400,600]
    column_list = get_cropped_columns(im, column_limits)
    expected_len = len(column_limits)
    assert  expected_len == len(column_list)
    counter = 0
    for column in column_list:
        #Test right dimensions
        if counter > 0:
            assert column.size[0] == round(column_limits[counter] - column_limits[counter-1])
        else:
            assert column.size[0] == round(column_limits[counter])
        #Test right color and pixel match
        assert column_list[counter].getcolors()[0][1] == dict_items_lst[counter][0] 
        assert column_list[counter].size == dict_items_lst[counter][1]
        assert len(column_list[counter].getcolors()) == 1
        assert column_list[counter].getcolors()[0][0] == column.size[0]*column.size[1]
        counter+=1

def test_extract_table_content():
    import pandas as pd
    from table_processing.Table import Table
    from table_processing.Table_Detector import Table_Detector

    t_name = 'test_extract_table_content'
    file_path = './tests/resources/' + t_name + '/'  + t_name
    trueT = pd.read_excel(file_path+'_true.xlsx', dtype=str)
    detc_table = Table_Detector(file_path+'.pdf')
    table = detc_table.get_page_data()[0]['tables'][0]['table_content']
    readT = Table.get_as_dataframe(table)

    assert len(trueT) == len(readT)  # matching row amount
    assert len(trueT.columns.values) == len(readT.columns.values)  # matching column amount

    correct_cells = {0:list(range(0,10)), 1:list(range(0,10)), 2:list(range(0,10)), 
                     3:list(range(0,10)), 4:[2,3,5,7,9]}
    for c in correct_cells.keys():
        for r in correct_cells[c]:
            assert str(trueT.iloc[r,c]) == str(readT.iloc[r,c])  # matching cell contents



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

def test_MultiPage():
    import PyPDF2
    #One page pdf file
    doc1 = open('tests/resources/DmZUHweaZfPcMjTCAySRtp.pdf', 'rb')
    #Four page pdf file
    doc2 = open('tests/resources/GBnzszrSV2sAXLEH5k7SFz.pdf', 'rb')
    
    pdfReader1 = PyPDF2.PdfReader(doc1)
    pdfReader2 = PyPDF2.PdfReader(doc2)

    # count number of pages
    totalPages1 = len(pdfReader1.pages)
    totalPages2 = len(pdfReader2.pages)
    
    assert totalPages1 == 1
    assert totalPages2 > 1


def test_metrics():
    import pandas as pd
    from table_processing.table_metrics import test_tables

    # Import true and processed tables
    t_name = 'test_metrics'
    file_path = './tests/resources/' + t_name + '/'  + t_name
    trueT = pd.read_excel(file_path+'_true.xlsx')
    readT = pd.read_excel(file_path+'.xlsx')
    metrics_df = test_tables({t_name: [trueT,readT]})

    assert metrics_df['Overlap'][t_name] == 1.000  # dimensions
    assert metrics_df['String Similarity'][t_name] == 0.888  # overall contents
    assert metrics_df['Completeness'][t_name] == 0.560  # cell content completeness
    assert metrics_df['Purity'][t_name] == 0.440  # cell content purity
    assert metrics_df['Precision'][t_name] == 0.225  # cell neighbours/location
    assert metrics_df['Recall'][t_name] == 0.225  # cell neighbours/location


# Test the input bulletproofing on process_pdf()
def test_process_pdf():
    from table_processing.Table_processor_main import process_pdf, default_output
    from pathlib import Path
    import os

    # Bad input path
    input_path = "./tests/resources"
    exception_happened = False
    try:
        process_pdf(input_path)
    except:
        exception_happened = True
    assert(exception_happened)

    # Good input path, good output path
    input_path = "./tests/resources/DmZUHweaZfPcMjTCAySRtp.pdf"
    output_path = "./tests/resources/out.xlsx"
    if os.path.exists(output_path):
        os.remove(output_path)
    returned_path = process_pdf(input_path, output_file_path = output_path)
    returned_path = Path(returned_path)
    assert(returned_path.match(output_path))
    assert(os.path.exists(output_path))
    os.remove(output_path)
    assert not os.path.exists(output_path)

    # Good input path, no provided output path
    input_path = "./tests/resources/DmZUHweaZfPcMjTCAySRtp.pdf"
    output_path = default_output
    if os.path.exists(output_path):
        os.remove(output_path)
    returned_path = process_pdf(input_path)
    returned_path = Path(returned_path)
    assert(returned_path.match(output_path))
    assert os.path.exists(output_path)
    os.remove(output_path)
    assert not os.path.exists(output_path)

    # Good input path, bad output path
    input_path = "./tests/resources/DmZUHweaZfPcMjTCAySRtp.pdf"
    expected_output_path = default_output
    output_path = "asdf"
    if os.path.exists(output_path):
        os.remove(output_path)
    returned_path = process_pdf(input_path, output_file_path = output_path)
    returned_path = Path(returned_path)
    assert(returned_path.match(expected_output_path))
    assert os.path.exists(expected_output_path)
    os.remove(expected_output_path)
    assert not os.path.exists(expected_output_path)


def test_process_content():
    from table_processing.Table_processor_main import process_content
    from pathlib import Path
    import os
    import fitz
    input_path = "./tests/resources/DmZUHweaZfPcMjTCAySRtp.pdf"
    output_path = "./tests/resources/out_test_process_content.xlsx"
    if os.path.exists(output_path):
        os.remove(output_path)
    doc = fitz.open(input_path)
    content = doc.tobytes() 
    doc.close()
    returned_path = process_content(content, output_file_path = output_path)
    returned_path = Path(returned_path)
    expected_output_path = output_path
    assert(returned_path.match(expected_output_path))
    assert os.path.exists(expected_output_path)
    os.remove(expected_output_path)
    assert not os.path.exists(expected_output_path)


def test_base64_input():
    from table_processing.Table_processor_main import process_content
    from pathlib import Path
    import os
    import fitz
    import base64    

    input_path = "./tests/resources/DmZUHweaZfPcMjTCAySRtp.pdf"
    output_path = "./tests/resources/test_base64_input.xlsx"
    if os.path.exists(output_path):
        os.remove(output_path)

    input_file = open(input_path,"rb")
    content_binary = input_file.read()
    data = (base64.b64encode(content_binary))
    content = base64.b64decode(data)

    returned_path = process_content(content, output_file_path = output_path)
    returned_path = Path(returned_path)
    expected_output_path = output_path

    assert(returned_path.match(expected_output_path))
    assert os.path.exists(expected_output_path)
    os.remove(expected_output_path)
    assert not os.path.exists(expected_output_path)


def test_clean_cell_text():
    import pandas as pd
    from table_processing.table_tools import clean_cell_text
    df_messy = pd.DataFrame([['asdf', 'asdf|', 'asdf'],['asdf', 'asdf', 'asdf']])
    df_messy.applymap(clean_cell_text)
    df_expected = pd.DataFrame([['asdf', 'asdf', 'asdf'],['asdf', 'asdf', 'asdf']])
    assert df_messy.compare(df_expected)

