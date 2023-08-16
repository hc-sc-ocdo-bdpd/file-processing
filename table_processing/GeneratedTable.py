import pylatex as pl
import shortuuid as sd
from pydbgen import pydbgen as dbgen
import os
import pandas as pd
import numpy as np
import random
import logging

myDB= dbgen.pydb()
col_list = ['country', 'city', 'zipcode', 'latitude', 'longitude','name_month', 'weekday', 'year', 'time', 'date', 'email','company', 'job_title', 'phone', 'license_plate'
           ]
            
class GeneratedTable:
    def __init__(self, rows=10, columns=5, row_lines=True, vertical_lines=True, margin='0.7in', multi_row=False, row_height=1.25, font_size=10, landscape=False): 
        # Store inputted generated table class parameters
        self.rows = rows
        self.columns = columns 
        self.row_lines = row_lines
        self.vertical_lines = vertical_lines
        self.font_size = font_size
        self.multi_row = multi_row
        self.geometry_options = {
            'margin':margin,
            'landscape':landscape
        }
        # Set parameter mins & maxes
        min_row_height = 1.25
        max_columns = 15
        
        if row_height < min_row_height:
            self.row_height = min_row_height
        else:
            self.row_height = row_height  # row height value is relative to font size (so automatically adjusts with it)

        if self.multi_row == True and (self.row_lines == False or self.vertical_lines == False):
            raise Exception('Cannot create table with multi-rows and with no vertical and horizontal lines')
        
        if self.columns > max_columns:
            self.columns = max_columns
            logging.warning('Cannot generate that many columns, shrunk down to ' + str(max_columns))

        # Trim row amount to keep table on one page
        landscape_mult = 0.7 if self.geometry_options['landscape'] else 1
        font_mult = np.exp(-0.05*self.font_size + 0.5)
        rheight_mult = 1 / self.row_height
        max_rows = max(int(40 * landscape_mult * font_mult * rheight_mult), 1)
        if self.rows > max_rows:
            self.rows = max_rows
            rows = max_rows
            logging.warning('Cannot generate that many rows on one page given table parameters, shrunk down to ' + str(max_rows))

        # Generate randomized table data
        self.generate_df(rows)

        if self.columns < columns:
            logging.warning('Generated table shrunk from ' + str(columns) + ' columns to ' + str(self.columns) + ' due to it overflowing off the page')
            columns = self.columns

        # Handle existence of column separator lines
        if self.vertical_lines ==  True:
            self.table_spec = '|c'
            self.table_spec = self.table_spec*self.columns + '|'
        else:
            self.table_spec = 'c'
            self.table_spec = self.table_spec*self.columns

    # Function to generate randomized table data
    def generate_df(self,rows):
        self.df = myDB.gen_dataframe(
        rows,fields=self.generate_fields(),
        real_email=False,phone_simple=True)
        # Multi-row handling
        if self.multi_row == True:
            for row in self.df.index:
                if row % 3 ==0:
                    self.df.loc[row,self.df.columns[0]] = ''

        # Trim column amount if table overflows outside of page
        landscape_mult = 1 if self.geometry_options['landscape'] else 0.7
        font_mult = np.exp(-0.05*self.font_size + 0.5)
        char_thresh = max(135 * landscape_mult * font_mult, 1)
        col_char_width = []
        for col in list(self.df.columns.values):
            col_char_width.append(max([len(str(col))] + self.df[col].astype(str).str.len().tolist()) + 2)  # max string length of column (or column name if bigger) plus 2 characters
        while (sum(col_char_width) > char_thresh) & (len(col_char_width) > 1):
            col_char_width = col_char_width[:-1]  # remove last column until table is below character threshold (or down to just 1 column)
        self.df = self.df[list(self.df.columns.values)[:len(col_char_width)]]
        self.columns = len(col_char_width)

        # Keep 'None' input instead of missing value
        self.df = self.df.astype(str)

    # Function to create pdf with generated table, done with pylatex (pl)
    def to_pdf(self):
        self.filename = sd.uuid()
        self.path = './generated_tables/' + self.filename + '/' + self.filename
        if not os.path.exists(self.path):
            os.makedirs('./generated_tables/' + self.filename)

        doc = pl.Document(geometry_options=self.geometry_options, font_size='')
        font_size = '\\fontsize{{{x}pt}}{{{x}}}\selectfont'.format(x=self.font_size)

        if self.row_lines == True and self.multi_row == False:
            with doc.create(pl.Center()) as centered:
                doc.append(pl.NoEscape(r'{font}'.format(font=font_size)))
                with centered.create(pl.LongTable(self.table_spec, row_height=self.row_height)) as table:
                    table.add_hline()
                    table.add_row(list(self.df.columns))
                    table.add_hline()
                    for row in self.df.index:
                        table.add_row(list(self.df.loc[row,:]))
                        table.add_hline()
                doc.generate_pdf(self.path, compiler='pdflatex', clean_tex='False')

        elif self.row_lines == True and self.multi_row == True :
            with doc.create(pl.Center()) as centered:
                doc.append(pl.NoEscape(r'{font}'.format(font=font_size)))
                with centered.create(pl.LongTable(self.table_spec)) as table:
                    table.add_hline()
                    table.add_row(list(self.df.columns))
                    table.add_hline()
                    for row in self.df.index:
                        if self.df.loc[row,self.df.columns[0]] == '':  # if current row first cell is empty
                            table.add_row(list(self.df.loc[row,:]))
                            if row == len(self.df.index)-1: # if last row
                                table.add_hline()
                            else:
                                try:
                                    if self.df.loc[row+1,self.df.columns[0]] != '' and self.df.loc[row-1,self.df.columns[0]] != '':
                                        table.add_hline()
                                    else:
                                        table.add_hline(start=2)
                                except Exception as e:  # case runs if current row is either last or first row
                                    table.add_hline(start=2)                       
                        else:
                            try: 
                                # look at next row if first for first cell empty
                                if self.df.loc[row+1,self.df.columns[0]] == '':
                        
                                    table.add_row(list(self.df.loc[row,:]))
                                    table.add_hline(start=2)
                                    continue
                                table.add_row(list(self.df.loc[row,:]))
                                table.add_hline()
                            except Exception as e:  # case runs if row is last row
                                table.add_row(list(self.df.loc[row,:]))
                                table.add_hline()
                doc.generate_pdf(self.path, compiler='pdflatex')

        else:
            with doc.create(pl.Center()) as centered:
                doc.append(pl.NoEscape(r'{font}'.format(font=font_size)))
                with centered.create(pl.LongTable(self.table_spec,row_height=self.row_height)) as table:
                    table.add_hline()
                    table.add_row(list(self.df.columns))
                    table.add_hline()
                    for row in self.df.index:
                        table.add_row(list(self.df.loc[row,:]))
                    table.add_hline()
            doc.generate_pdf(self.path, compiler='pdflatex')


    def get_path(self):
        return self.path

    def get_filename(self):
        return self.filename
    
    def generate_fields(self):
        fields = ['name']
        tmp_list = random.sample(col_list, self.columns-1)
        fields = fields + tmp_list
        return fields
    
    # Function to store all parameters for generated table, useful for model performance testing in metrics sheet
    def get_params(self):
        param_dict = {'filename':self.filename, 'rows':self.rows, 'columns':self.columns, 'row_lines':self.row_lines, 
                      'vertical_lines':self.vertical_lines, 'margin':self.geometry_options['margin'], 
                      'multi_row':self.multi_row, 'row_height':self.row_height, 'font_size':self.font_size, 
                      'landscape':self.geometry_options['landscape']}
        return param_dict



   
