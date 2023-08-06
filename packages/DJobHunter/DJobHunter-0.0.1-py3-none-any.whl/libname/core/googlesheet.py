import os
import json
import gspread
from gspread import Cell
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials


class BaseSpreadsheet:
    def __init__(self):
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        service_account_credentials = json.load(open('./google_service.json'))
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(service_account_credentials, scope)
        self.gc = gspread.authorize(credentials)
        self.sh = self.gc.open_by_url(self.get_google_sheet_url())
        self.data_sheet = self.sh.worksheet(self.get_sheet_name())
        self.write_headers()

    def write_headers(self):
        cells = []
        headers = self.get_header()
        for i, header in enumerate(headers):
            cells.append(
                Cell(
                    row=1,
                    col=i+1,
                    value=header
                )
            )
        self.data_sheet.update_cells(cells)

    def get_sheet_name(self):
        raise NotImplemented

    def get_google_sheet_url(self):
        raise NotImplemented

    def get_header(self):
        raise NotImplemented
    
    def get_all_records(self):
        return self.data_sheet.get_all_records()