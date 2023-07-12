
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

