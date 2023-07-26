import pydbgen
import pylatex as pl
import shortuuid as sd
from pydbgen import pydbgen as dbgen
import pandas as pd
import numpy as np


myDB= dbgen.pydb()

class GeneratedTable:
    def __init__(self,rows=10,columns=5,row_lines = None, vertical_lines = None, margin='0.7in', multi_row = None): 
        self.rows = rows
        self.columns = columns 
        self.row_lines = row_lines
        self.vertical_lines = vertical_lines
        self.geometry_options = {
            'vmargin':margin
        }
        self.multi_row = multi_row

        if self.vertical_lines ==  True:
            self.table_spec = 'c|c|c|c|c'
        else:
            self.table_spec = 'ccccc'

        if self.multi_row == True and self.row_lines == False and self.vertical_lines == False:
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
        print(self.df)

        
          

    def to_pdf(self):
        doc = pl.Document(geometry_options=self.geometry_options)  

        if self.row_lines == True and self.multi_row == False:
            
            with doc.create(pl.Center()) as centered:
                with centered.create(pl.Tabu(self.table_spec)) as table:
                    #table.add_hline()
                    table.add_row(list(self.df.columns))
                    table.add_hline()
                    for row in self.df.index:
                        print(row)
                        table.add_row(list(self.df.loc[row,:]))
                        table.add_hline()
                    #table.add_hline()

                self.filename = sd.uuid()

                self.path = './generated_tables/' + self.filename 

                doc.generate_pdf(self.path, compiler='pdflatex')
                self.path += '.pdf'

        elif self.row_lines == True and self.multi_row == True :
            with doc.create(pl.Section('Table')):
                with doc.create(pl.Tabu(self.table_spec)) as table:
                    #table.add_hline()
                    table.add_row(list(self.df.columns))
                    table.add_hline()
                    for row in self.df.index:
                        if self.df.loc[row,self.df.columns[0]] == '':
                            #add row and hline(start=2)
                            table.add_row(list(self.df.loc[row,:]))
                            if row == len(self.df.index)-1:
                                print('yes', row, len(self.df.index))
                                table.add_hline()
                            else:
                                try:
                                    if self.df.loc[row+1,self.df.columns[0]] != '' and self.df.loc[row-1,self.df.columns[0]] != '':
                                        table.add_hline()
                                    else:
                                        table.add_hline(start=2)
                                    print('nooo', row, len(self.df.index))
                                except Exception as e:
                                    table.add_hline(start=2)

                                
                        else:
                            try: 
                            #   look at next row if first for first cell empty: ''
                                if self.df.loc[row+1,self.df.columns[0]] == '':
                            #       add row and hline(start=2)
                                    table.add_row(list(self.df.loc[row,:]))
                                    table.add_hline(start=2)
                                    continue
                                table.add_row(list(self.df.loc[row,:]))
                                table.add_hline()
                            except Exception as e:
                                table.add_row(list(self.df.loc[row,:]))
                                table.add_hline()
                
                    
                        #table.add_row(list(self.df.loc[row,:]))
                        #table.add_hline()
                    #table.add_hline()

                self.filename = sd.uuid()

                self.path = './generated_tables/' + self.filename 

                doc.generate_pdf(self.path, compiler='pdflatex')
                self.path += '.pdf'


        else:
            with doc.create(pl.Center()) as centered:
                with centered.create(pl.Tabu(self.table_spec)) as table:
                    table.add_hline()
                    table.add_row(list(self.df.columns))
                    table.add_hline()
                    for row in self.df.index:
                        print(row)
                        table.add_row(list(self.df.loc[row,:]))
                    table.add_hline()

            self.filename = sd.uuid()

            self.path = './generated_tables/' + self.filename 

            doc.generate_pdf(self.path, compiler='pdflatex')
            self.path += '.pdf'

    def get_path(self):
        return self.path
    
    def get_filename(self):
        return self.filename
        
   
    

