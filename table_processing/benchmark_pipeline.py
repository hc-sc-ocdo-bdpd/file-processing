from GeneratedTable import GeneratedTable
from Table_Detector import Table_Detector


test_table = GeneratedTable(rows=35, row_height=3.5)
test_table.to_pdf_longtable()

# table_det = Table_Detector(test_table.get_path())
# table_det.to_excel(test_table.get_path().split('.pdf')[0]+'.xlsx')

