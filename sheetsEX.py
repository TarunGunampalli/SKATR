import gspread
#import pandas as pd 
from oauth2client.service_account import ServiceAccountCredentials 

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope) #has info for service account
client = gspread.authorize(creds)

users_sheet = client.open("SKATRdb").get_worksheet(0)
survey_sheet = client.open("SKATRdb").get_worksheet(2)