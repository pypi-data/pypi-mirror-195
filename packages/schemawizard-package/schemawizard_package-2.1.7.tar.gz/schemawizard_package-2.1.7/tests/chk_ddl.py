"""
  Dave Skura
  
  File Description:
"""
from schemawizard_package.schemawizard import schemawiz
csvfilename = 'sample.csv'
print ("checking csv file " + csvfilename) # 

schwiz = schemawiz()

schwiz.loadcsvfile(csvfilename)

postgres_ddl = schwiz.guess_postgres_ddl(csvfilename.replace('.','_'))

print(postgres_ddl)



