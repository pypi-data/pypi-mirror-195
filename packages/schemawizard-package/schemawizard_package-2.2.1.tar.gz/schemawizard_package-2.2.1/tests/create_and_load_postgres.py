"""
  Dave Skura
"""
from schemawizard_package.schemawizard import schemawiz

csvfilename = 'tesla.csv'

obj = schemawiz()

r = schemawiz().createload_postgres_from_csv(csvfilename)

print(r + ' created.')

