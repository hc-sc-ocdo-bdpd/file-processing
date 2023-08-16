import pandas as pd
from Levenshtein import distance as lev_dist

def overlap(df1, df2):
    # Find intersection area (mulitplication of dim mins)
    xmin = min(df1.shape[0], df2.shape[0])
    ymin = min(df1.shape[1], df2.shape[1])
    intersection = xmin*ymin
    # Find union area (multiplication of dim maxs minus multiplication of dim max-min diffs)
    xmax = max(df1.shape[0], df2.shape[0])
    ymax = max(df1.shape[1], df2.shape[1])
    union = xmax*ymax - (xmax-xmin)*(ymax-ymin)
    # Calculate overlap
    overlap_pct = intersection / union
    return round(overlap_pct, 3)

def string_similarity(df1, df2):
    # Transform tables to strings
    str1 = df1.to_string()
    str2 = df2.to_string()
    # Calculate string similarity
    edits_per_char = lev_dist(str1, str2) / max(len(str1), len(str2))
    return round(1-edits_per_char, 3)

def completeness(df1, df2):
    # Transform tables to lists of lists
    vals1 = df1.values.tolist()
    vals2 = df2.values.tolist()
    # Initialize numerator & denominator counters
    compl_count = 0
    real_total = df1.size
    # Loop through values
    for i in range(0, len(vals1)):
        row = vals1[i]
        for j in range(0, len(row)):
            cell1 = row[j]
            # Verify if cell1 is contained in cell2 (completely identified)
            try:
                cell2 = vals2[i][j]
                if cell1 in cell2:
                    compl_count += 1
            except IndexError:
                pass
    # Calculate completeness
    completeness_score = compl_count / real_total
    return round(completeness_score, 3)

def purity(df1, df2):
    # Transform tables to lists of lists
    vals1 = df1.values.tolist()
    vals2 = df2.values.tolist()
    # Initialize numerator & denominator counters
    pure_count = 0
    detected_total = df2.size
    # Loop through values
    for i in range(0, len(vals2)):
        row = vals2[i]
        for j in range(0, len(row)):
            cell2 = row[j]
            # Verify if cell2 is contained in cell1 (purely detected)
            try:
                cell1 = vals1[i][j]
                if cell2 in cell1:
                    pure_count += 1
            except IndexError:
                pass
    # Calculate purity
    purity_score = pure_count / detected_total
    return round(purity_score, 3)

def precision(df1, df2):
    # Transform tables to lists of lists
    vals1 = df1.values.tolist()
    vals2 = df2.values.tolist()
    r,c = df2.shape
    # Initialize numerator & denominator counters
    correct_pl = 0
    detected_pl = 2*r*c - r - c
    # Loop through connections within rows
    for i in range(0, len(vals2)):
        row = vals2[i]
        for j in range(0, len(row)-1):
            cells2 = row[j:j+2]
            # Verify if pair of cells2 is equal to pair of cells1 (correct PL)
            try:
                cells1 = vals1[i][j:j+2]
                if cells2 == cells1:
                    correct_pl += 1
            except IndexError:
                pass
    # Loop through connections within columns
    tvals1 = df1.transpose().values.tolist()
    tvals2 = df2.transpose().values.tolist()
    for i in range(0, len(tvals2)):
        col = tvals2[i]
        for j in range(0, len(col)-1):
            cells2 = col[j:j+2]
            # Verify if pair of cells2 is equal to pair of cells1 (correct PL)
            try:
                cells1 = tvals1[i][j:j+2]
                if cells2 == cells1:
                    correct_pl += 1
            except IndexError:
                pass
    # Calculate precision
    if df2.shape == (1,1):  # account for lack of neighbours in 1x1 dataframes (so zero proto-links)
        precision_score = 1
    else:
        precision_score = correct_pl / detected_pl
    return round(precision_score, 3)

def recall(df1, df2):
    # Transform tables to lists of lists
    vals1 = df1.values.tolist()
    vals2 = df2.values.tolist()
    r,c = df1.shape
    # Initialize numerator & denominator counters
    correct_pl = 0
    total_pl = 2*r*c - r - c
    # Loop through connections within rows
    for i in range(0, len(vals1)):
        row = vals1[i]
        for j in range(0, len(row)-1):
            cells1 = row[j:j+2]
            # Verify if pair of cells1 is equal to pair of cells2 (correct PL)
            try:
                cells2 = vals2[i][j:j+2]
                if cells1 == cells2:
                    correct_pl += 1
            except IndexError:
                pass
    # Loop through connections within columns
    tvals1 = df1.transpose().values.tolist()
    tvals2 = df2.transpose().values.tolist()
    for i in range(0, len(tvals1)):
        col = tvals1[i]
        for j in range(0, len(col)-1):
            cells1 = col[j:j+2]
            # Verify if pair of cells1 is equal to pair of cells2 (correct PL)
            try:
                cells2 = tvals2[i][j:j+2]
                if cells1 == cells2:
                    correct_pl += 1
            except IndexError:
                pass
    # Calculate recall
    if df1.shape == (1,1):  # account for lack of neighbours in 1x1 dataframes (so zero proto-links)
        recall_score = 1
    else:
        recall_score = correct_pl / total_pl
    return round(recall_score, 3)

def all_metrics(df1, df2):
    # Clean & format dataframes
    df1 = df1.fillna('').astype(str)
    df2 = df2.fillna('').astype(str)
    # Run all metric functions
    results = {'Overlap':            overlap(df1, df2),
               'String Similarity':  string_similarity(df1, df2), 
               'Completeness':       completeness(df1, df2),
               'Purity':             purity(df1, df2),
               'Precision':          precision(df1, df2),
               'Recall':             recall(df1, df2)}
    return results

def test_tables(tables):
    # Initialize list to store metrics/results
    results_lst = []
    # Run all metrics for each table
    for t in tables:
        df1, df2 = tables[t]
        # Skip metrics if table has 0x0 dimensions
        if (df1.shape == (0,0)) | (df2.shape == (0,0)):  
            results_lst.append({'Overlap':0, 'String Similarity':0, 'Completeness':0, 
                                'Purity':0, 'Precision':0, 'Recall':0})
        else:
            results_lst.append(all_metrics(df1, df2))
    # Return dataframe with all metrics (columns) for each table (rows)
    return pd.DataFrame(results_lst, index=tables.keys())