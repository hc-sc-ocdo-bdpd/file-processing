# Import table classes, functions, and packages
from GeneratedTable import GeneratedTable
from Table_Detector import Table_Detector
from table_metrics import test_tables
import pandas as pd
import numpy as np
import random
# xlsxwriter not imported, but needs to be downloaded in environment
import logging
logging.basicConfig(filename='benchmarking_log', filemode='a', datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.WARNING, format='[%(asctime)s][%(levelname)s] %(message)s\n')

# Manual setting variables
n = 1  # number of tables to generate
randomize_all_parameters = True  # if all generated table parameters should be randomized

# Initialize variables
tables = {}
failed_tables = []
gen_params = []

# Loop for n # of tables
for i in range(0,n):
    # Generate table, store, and export to pdf true table
    if randomize_all_parameters:
        genr_table = GeneratedTable(rows=random.randint(1, 50), columns=random.randint(1, 20), row_lines=bool(random.getrandbits(1)), vertical_lines=bool(random.getrandbits(1)), margin=str(random.randint(0, 10)/10)+'in', multi_row=False, row_height=random.randint(25, 50)/20, font_size=random.randint(6, 20), landscape=bool(random.getrandbits(1)))
    else:
        genr_table = GeneratedTable(rows=10, columns=5, row_lines=True, vertical_lines=True, margin='0.7in', multi_row=False, row_height=1.25, font_size=10, landscape=False)
    # Store & export pdf and .xlsx versions of generated table
    true_table = genr_table.df
    genr_table.to_pdf()
    gen_params.append(genr_table.get_params())  # store generated table parameters
    t_name = genr_table.get_filename()
    logging.warning('Generated table ' + t_name)
    file_path = 'generated_tables/' + t_name + '/'  + t_name
    true_table.to_excel(file_path + '_true.xlsx', index = False)
    # Detect table from pdf, export to and read from excel processed table
    try:
        detc_table = Table_Detector(file_path+'.pdf')  # run table detector model on pdf
        table = detc_table.get_page_data()[0]['tables'][0]['table_content']
        detc_table.to_excel(file_path+'.xlsx')
        read_table = pd.read_excel(file_path+'.xlsx', dtype=str)  # force extract text as string (otherwise there may be errors with some numbers)
        detc_table.output_table_steps(file_path+'_intermediate_output/')
    except IndexError:  # could not detect table from pdf
        logging.error('Could not detect table from pdf ' + t_name)
        read_table = pd.DataFrame()
        failed_tables.append(t_name)
        logging.error('Could not detect table ' + t_name + ' from pdf')
    tables[t_name] = [true_table, read_table]

# Calculate table extraction performance metrics and format output dfs
metrics_df = test_tables(tables)  # metrics function
metrics_df.loc[metrics_df.index.isin(failed_tables), list(metrics_df.columns.values)] = 0  # deal with failed detection tables
summary_df = metrics_df.astype(float).describe().fillna(0).apply(lambda s: s.apply('{0:.3f}'.format))  
summary_df.loc[summary_df.index == 'count'] = summary_df.loc[summary_df.index == 'count'].astype(float).astype(int).astype(str)  # format count column
summary_df = summary_df.reset_index().rename(columns={'index':''})
metrics_df = metrics_df.apply(lambda s: s.apply('{0:.3f}'.format)).reset_index().rename(columns={'index':'filename'})  # number formatting
logging.warning(pd.DataFrame(np.row_stack((summary_df.columns, summary_df.to_numpy())),    # log metrics summary
                columns=['']*len(summary_df.columns), index=['']*(1+len(summary_df))))

# Add generated parameters to metrics sheet to allow identification of well & poor performing tables by characteristics
metrics_df = pd.merge(metrics_df, pd.DataFrame(gen_params), on = 'filename', how = 'left')

# Function to export excel files with auto-formatting
def write_report(exported_df, exported_dfName):
    global writerFinal
    exported_df.to_excel(writerFinal, exported_dfName, index = False)
    for idx, col in enumerate(exported_df):
        series = exported_df[col]
        max_len = max((series.astype(str).map(len).max(), len(str(series.name)))) + 1.5
        writerFinal.sheets[exported_dfName].set_column(idx, idx, max_len)

# Export metrics data
try:
    writerFinal = pd.ExcelWriter('table_metrics.xlsx')
    write_report(metrics_df, 'All Tables'), write_report(summary_df, 'Metrics Summary')
    writerFinal.close()
except PermissionError:
    logging.error('Metrics sheet could not be exported due to excel file already being open')
except AttributeError:
    logging.error('Metrics sheet could not be exported due to the "xlsxwriter" package not being downloaded in the environment')