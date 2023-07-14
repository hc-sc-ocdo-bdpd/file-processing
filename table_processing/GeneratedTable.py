import pydbgen
import pylatex as pl
import shortuuid as sd
from pydbgen import pydbgen as dbgen
import os
import pdflatex

myDB= dbgen.pydb()

class GeneratedTable:
    def __init__(self,rows=10,columns=5):    
       self.generate_df(rows)


    def generate_df(self,rows):
        self.df = myDB.gen_dataframe(
        rows,fields=['name','city','phone',
        'license_plate','email'],
        real_email=False,phone_simple=True
        )
          

    def to_pdf(self):
        doc = pl.Document()

        with doc.create(pl.Section('Table')):
            with doc.create(pl.Tabular('ccccc')) as table:
                table.add_hline()
                table.add_row(list(self.df.columns))
                table.add_hline()
                for row in self.df.index:
                    print(row)
                    table.add_row(list(self.df.loc[row,:]))
                table.add_hline()

        self.filename = sd.uuid()

        doc.generate_tex(self.filename)
        self.filename +='.tex'
        os.system('pdflatex ' + self.filename)


t1 = GeneratedTable()
t1.to_pdf()