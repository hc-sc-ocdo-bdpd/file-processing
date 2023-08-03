# Import table classes, functions, and packages
from GeneratedTable import GeneratedTable
from Table_Detector import Table_Detector
from table_metrics import test_tables
import pandas as pd
import numpy as np
# xlsxwriter not imported, but needs to be downloaded in environment
import logging
logging.basicConfig(filename='benchmarking_log', filemode='a', datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.WARNING, format='[%(asctime)s][%(levelname)s] %(message)s\n')

# Initialize table dict
tables = {}
failed_tables = []

# Loop for n # of tables
for i in range(0,1):
    # Generate, store, and export to pdf true table
    genr_table = GeneratedTable(rows=5, columns=5, row_lines=True, vertical_lines=True, multi_row=False, row_height=1)
    true_table = genr_table.df
    genr_table.to_pdf()
    t_name = genr_table.get_filename()
    logging.warning('Generated table ' + t_name)
    file_path = 'generated_tables/' + t_name + '/'  + t_name
    true_table.to_excel(file_path + '_true.xlsx', index = False)
    # Detect from pdf, export to and read from excel processed table
    try:
        detc_table = Table_Detector(file_path+'.pdf')
        table = detc_table.get_page_data()[0]['tables'][0]['table_content']
        boxes_image = table.plot_bounding_boxes(file_name = file_path+'_boxes')
        detc_table.to_excel(file_path+'.xlsx')
        read_table = pd.read_excel(file_path+'.xlsx')
        # Store true and read tables
    except IndexError:  # could not detect table from pdf
        read_table = pd.DataFrame()
        failed_tables.append(t_name)
        logging.error('Could not detect table ' + t_name + ' from pdf')
    tables[t_name] = [true_table, read_table]

# Calculate table extraction performance metrics and format output dfs
metrics_df = test_tables(tables)
metrics_df.loc[metrics_df.index.isin(failed_tables), list(metrics_df.columns.values)] = 0
summary_df = metrics_df.astype(float).describe().fillna(0).apply(lambda s: s.apply('{0:.3f}'.format))
summary_df.loc[summary_df.index == 'count'] = summary_df.loc[summary_df.index == 'count'].astype(float).astype(int).astype(str)
summary_df = summary_df.reset_index().rename(columns={'index':''})
metrics_df = metrics_df.apply(lambda s: s.apply('{0:.3f}'.format)).reset_index().rename(columns={'index':'ID'})
logging.warning(pd.DataFrame(np.row_stack((summary_df.columns, summary_df.to_numpy())), 
                columns=['']*len(summary_df.columns), index=['']*(1+len(summary_df))))

# Export metrics
def write_report(exported_df, exported_dfName):
    global writerFinal
    exported_df.to_excel(writerFinal, exported_dfName, index = False)
    for idx, col in enumerate(exported_df):
        series = exported_df[col]
        max_len = max((series.astype(str).map(len).max(), len(str(series.name)))) + 1.5
        writerFinal.sheets[exported_dfName].set_column(idx, idx, max_len)
try:
    writerFinal = pd.ExcelWriter('table_metrics.xlsx')
    write_report(metrics_df, 'All Tables'), write_report(summary_df, 'Metrics Summary')
    writerFinal.close()
except PermissionError:
    logging.error('Metrics sheet could not be exported due to excel file already being open')
except AttributeError:
    logging.error('Metrics sheet could not be exported due to the "xlsxwriter" package not being downloaded in the environment')