# Import packages
import pandas as pd
import os

# Function to export excel files with auto-formatting
def write_report(exported_df, exported_dfName):
    global writerFinal
    exported_df.to_excel(writerFinal, exported_dfName, index = False)
    for idx, col in enumerate(exported_df):
        series = exported_df[col]
        max_len = max((series.astype(str).map(len).max(), len(str(series.name)))) + 1.5
        writerFinal.sheets[exported_dfName].set_column(idx, idx, max_len)

# Get all sheets from randomized generation tests
path = r'table_trials_results/'
xlsx_sheets = os.listdir(path)
xlsx_sheets = [x for x in xlsx_sheets if '.xlsx' in x]
if 'table_metrics_ALL.xlsx' in xlsx_sheets: xlsx_sheets.remove('table_metrics_ALL.xlsx')
all_tables = pd.DataFrame()

# Loop through sheets and add all to consolidated df
for sheet in xlsx_sheets:
    df = pd.read_excel(path+sheet, 'All Tables')
    if 'special_characters_emphasis' not in df.columns.values:
        df['special_characters_emphasis'] = False   # add special_characters_emphasis column if not already in df
    all_tables = pd.concat([all_tables, df])
met_cols = all_tables.columns.values.tolist()[1:7]
all_data = all_tables.drop(columns=['filename'])
all_tables[met_cols] = all_tables[met_cols].apply(lambda s: s.apply('{0:.3f}'.format))

# Create metrics summary df
summary_df = all_data[met_cols].astype(float).describe().fillna(0).apply(lambda s: s.apply('{0:.3f}'.format))
summary_df.loc[summary_df.index == 'count'] = summary_df.loc[summary_df.index == 'count'].astype(float).astype(int).astype(str)
summary_df = summary_df.reset_index().rename(columns={'index':''})

# Create df of results by individual parameters
ind_results = pd.DataFrame(data=[], columns = ['Parameter', 'Value']+met_cols+['Count'])
for param in all_data.columns.values.tolist()[6:]:
    param_results  = all_data[[param]+all_data.columns.values.tolist()[:6]].groupby([param]).mean().reset_index().rename(columns={param:'Value'})
    param_results['Count']  = all_data.groupby([param]).agg('count').reset_index(drop=True)['Overlap']
    param_results.insert(0, 'Parameter', param)
    ind_results = pd.concat([ind_results, param_results])
ind_results.reset_index(drop=True, inplace=True)
ind_results[met_cols] = ind_results[met_cols].apply(lambda s: s.apply('{0:.3f}'.format))

# Create df of results by combination of parameters
comb_results = all_data.groupby(all_data.columns.values.tolist()[6:]).mean().reset_index()
comb_results['Count'] = all_data.groupby(all_data.columns.values.tolist()[6:]).agg('count').reset_index(drop=True)['Overlap']
comb_results[met_cols] = comb_results[met_cols].apply(lambda s: s.apply('{0:.3f}'.format))

# Export all
writerFinal = pd.ExcelWriter(path + 'table_metrics_ALL.xlsx')
write_report(all_tables, 'All Tables')
write_report(summary_df, 'Metrics Summary')
write_report(ind_results, 'Results by Parameter')
write_report(comb_results, 'Results by Combination')
writerFinal.close()