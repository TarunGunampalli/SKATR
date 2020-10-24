#pip install gspread
#pip install --upgrade google-api-python-client oauth2client

import gspread
#import pandas as pd 
from oauth2client.service_account import ServiceAccountCredentials 

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope) #has info for service account
client = gspread.authorize(creds)

sheet = client.open("commentary data").sheet1   #commentary data is a test sheet full of cricket plays

list_of_hashes = sheet.get_all_records()
print(list_of_hashes)

#sheet.get_all_values() list of lists instead of hashes
#Or you could just pull the data from a single row, column, or cell:

#sheet.row_values(1) select a row

#sheet.col_values(1) select a column probably most useful

#sheet.cell(1, 1).value select single cell