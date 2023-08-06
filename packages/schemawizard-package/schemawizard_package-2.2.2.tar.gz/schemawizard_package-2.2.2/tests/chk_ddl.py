"""
  Dave Skura
"""
from schemawizard_package.schemawizard import schemawiz
csvfilename = 'sample.csv'

postgres_ddl = schemawiz(csvfilename).guess_postgres_ddl()
#postgres_ddl = schemawiz(csvfilename).guess_postgres_ddl(csvfilename.replace('.','_'))

print(postgres_ddl)



