# Import table classes, functions, and packages
from GeneratedTable import GeneratedTable
from Table_Detector import Table_Detector
from table_metrics import test_tables
import pandas as pd

# Initialize table dict
tables = {}
failed_tables = []

# Loop for n # of tables
for i in range(0,1):
    # Generate, store, and export to pdf true table
    genr_table = GeneratedTable(5, row_lines=True, vertical_lines=True)
    true_table = genr_table.df
    genr_table.to_pdf()
    t_name = genr_table.filename
    # Detect from pdf, export to and read from excel processed table
    try:
        detc_table = Table_Detector(genr_table.get_path())
        xlsx_path = genr_table.get_path().split('.pdf')[0]+'.xlsx'
        detc_table.to_excel(xlsx_path)
        read_table = pd.read_excel(xlsx_path)
        # Store true and read tables
    except IndexError:  # could not detect table from pdf
        read_table = pd.DataFrame()
        failed_tables.append(t_name)
    tables[t_name] = [true_table, read_table]

# Calculate table extraction performance metrics
metrics_df = test_tables(tables)
metrics_df.loc[metrics_df.index.isin(failed_tables), list(metrics_df.columns.values)] = 0
summary_df = metrics_df.astype(float).describe().apply(lambda s: s.apply('{0:.4f}'.format))
print(metrics_df)
#print(summary_df)

# Export metrics
sheet_dfs = {'All Table Metrics':metrics_df, 'Metric Summaries':summary_df}
with pd.ExcelWriter('table_metrics.xlsx') as writer:
    for sheet in sheet_dfs:
        sheet_dfs[sheet].to_excel(writer, sheet)