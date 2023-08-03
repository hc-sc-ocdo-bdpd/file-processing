import pydbgen
import pylatex as pl
import shortuuid as sd
from pydbgen import pydbgen as dbgen
import os
import pandas as pd
import numpy as np

myDB= dbgen.pydb()

geometry_options = {'margin': '0.7in'}

class GeneratedTable:
    def __init__(self, rows=5, columns=5, row_lines=None, vertical_lines=None, margin='0.7in', multi_row=False, row_height=1): 
        self.rows = rows
        self.columns = columns 
        self.row_lines = row_lines
        self.vertical_lines = vertical_lines
        self.geometry_options = {
            'vmargin':margin
        }
        self.multi_row = multi_row
        self.row_height = row_height

        if self.vertical_lines ==  True:
            self.table_spec = 'c|c|c|c|c'
        else:
            self.table_spec = 'ccccc'
            
        if self.multi_row == True and (self.row_lines == False or self.vertical_lines == False):
            raise Exception('Cannot create table with multi-rows with no vertical and horizantal lines')

        self.generate_df(rows)


    def generate_df(self,rows):
        self.df = myDB.gen_dataframe(
        rows,fields=['name','city','phone',
        'license_plate','email'],
        real_email=False,phone_simple=True)

        if self.multi_row == True:
            for row in self.df.index:
                if row % 3 ==0:
                    self.df.loc[row,self.df.columns[0]] = ''
        

    def to_pdf(self):
        self.filename = sd.uuid()
        self.path = './generated_tables/' + self.filename + '/' + self.filename
        if not os.path.exists(self.path):
            os.makedirs('./generated_tables/' + self.filename)

        doc = pl.Document(geometry_options=self.geometry_options)
        if self.row_lines == True and self.multi_row == False:
            with doc.create(pl.Center()) as centered:
                with centered.create(pl.LongTable(self.table_spec, row_height=self.row_height)) as table:
                    table.add_row(list(self.df.columns))
                    table.add_hline()
                    for row in self.df.index:
                        table.add_row(list(self.df.loc[row,:]))
                        table.add_hline()
                doc.generate_pdf(self.path, compiler='pdflatex')

        elif self.row_lines == True and self.multi_row == True :
            with doc.create(pl.Center()) as centered:
                with centered.create(pl.LongTable(self.table_spec)) as table:
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
        
   
