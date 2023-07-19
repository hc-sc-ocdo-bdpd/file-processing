from GeneratedTable import GeneratedTable
from Table_Detector import Table_Detector


test_table = GeneratedTable(5, row_lines=True, vertical_lines=True)
test_table.to_pdf()

# table_det = Table_Detector(test_table.get_path())
# table_det.to_excel(test_table.get_path().split('.pdf')[0]+'.xlsx')

