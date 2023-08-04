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
    def __init__(self, rows=10, columns=5, row_lines=None, vertical_lines=None, margin='0.7in', multi_row=False, row_height=None, font_size=12, landscape=False): 
        self.rows = rows
        self.columns = columns 
        self.row_lines = row_lines
        self.vertical_lines = vertical_lines
        self.font_size = font_size
        self.geometry_options = {
            'margin':margin,
            'landscape':landscape
        }
        self.multi_row = multi_row
        
        if row_height is None:
            self.row_height = self.font_size/12
        else:
            self.row_height = row_height

        if self.multi_row == True and (self.row_lines == False or self.vertical_lines == False):
            raise Exception('Cannot create table with multi-rows and with no vertical and horizontal lines')
        
        if self.columns > 15:
            self.columns = 15
            logging.warning('Cannot generate that many columns, shrunk down to 15')

        self.generate_df(rows)

        if self.columns < columns:
            logging.warning('Generated table shrunk from ' + str(columns) + ' columns to ' + str(self.columns) + ' due to it overflowing off the page')

        if self.vertical_lines ==  True:
            self.table_spec = '|c'
            self.table_spec = self.table_spec*self.columns + '|'
        else:
            self.table_spec = 'c'
            self.table_spec*self.columns


    def generate_df(self,rows):
        self.df = myDB.gen_dataframe(
        rows,fields=self.generate_fields(),
        real_email=False,phone_simple=True)

        if self.multi_row == True:
            for row in self.df.index:
                if row % 3 ==0:
                    self.df.loc[row,self.df.columns[0]] = ''

        # Trim column amount if table overflows outside of page
        landscape_mult = 1 if self.geometry_options['landscape']==True else 110/150
        char_thresh = 150 * landscape_mult * 12/self.font_size
        col_char_width = []
        for col in list(self.df.columns.values):
            col_char_width.append(max([len(str(col))] + self.df[col].astype(str).str.len().tolist()) + 2)  # max string length of column (or column name if bigger) plus 2 characters
        while (sum(col_char_width) > char_thresh) & (len(col_char_width) > 1):
            col_char_width = col_char_width[:-1]  # remove last column until table is below character threshold (or down to just 1 column)
        self.df = self.df[list(self.df.columns.values)[:len(col_char_width)]]
        self.columns = len(col_char_width)

        # Keep 'None' input instead of missing value
        self.df = self.df.astype(str)

    def to_pdf(self):
        self.filename = sd.uuid()
        self.path = './generated_tables/' + self.filename + '/' + self.filename
        if not os.path.exists(self.path):
            os.makedirs('./generated_tables/' + self.filename)

        doc = pl.Document(geometry_options=self.geometry_options, font_size='')
        if self.row_lines == True and self.multi_row == False:
            with doc.create(pl.Center()) as centered:
                with centered.create(pl.LongTable(self.table_spec, row_height=self.row_height)) as table:
                    table.add_hline()
                    table.add_row(list(self.df.columns))
                    table.add_hline()
                    for row in self.df.index:
                        table.add_row(list(self.df.loc[row,:]))
                        table.add_hline()
                doc.generate_pdf(self.path, compiler='pdflatex')

        elif self.row_lines == True and self.multi_row == True :
            with doc.create(pl.Center()) as centered:
                with centered.create(pl.LongTable(self.table_spec)) as table:
                    table.add_hline()
                    table.add_row(list(self.df.columns))
                    table.add_hline()
                    for row in self.df.index:
                        if self.df.loc[row,self.df.columns[0]] == '':# if current row first cell is empty
                            table.add_row(list(self.df.loc[row,:]))
                            if row == len(self.df.index)-1: #if last row
                                table.add_hline()
                            else:
                                try:
                                    if self.df.loc[row+1,self.df.columns[0]] != '' and self.df.loc[row-1,self.df.columns[0]] != '':
                                        table.add_hline()
                                    else:
                                        table.add_hline(start=2)
                                except Exception as e:#case runs if current row is either last or first row
                                    table.add_hline(start=2)                       
                        else:
                            try: 
                            #   look at next row if first for first cell empty
                                if self.df.loc[row+1,self.df.columns[0]] == '':
                        
                                    table.add_row(list(self.df.loc[row,:]))
                                    table.add_hline(start=2)
                                    continue
                                table.add_row(list(self.df.loc[row,:]))
                                table.add_hline()
                            except Exception as e: #case runs if row is last row
                                table.add_row(list(self.df.loc[row,:]))
                                table.add_hline()
                doc.generate_pdf(self.path, compiler='pdflatex')

        else:
            with doc.create(pl.Center()) as centered:
                with centered.create(pl.LongTable(self.table_spec,row_height=self.row_height)) as table:

                    table.add_hline()
                    print(self.df)
                    print(self.columns)
                    print(self.df.columns)
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


   
