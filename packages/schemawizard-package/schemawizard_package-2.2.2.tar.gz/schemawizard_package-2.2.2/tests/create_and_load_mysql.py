"""
  Dave Skura
"""
from schemawizard_package.schemawizard import schemawiz

csvfilename = 'tesla.csv'

r = schemawiz().createload_mysql_from_csv(csvfilename)

print(r + ' created.')

