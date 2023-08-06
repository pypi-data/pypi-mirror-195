import os, json, requests
from typing import List, Dict, Callable, Tuple
from dotenv import load_dotenv
from core.googlesheet import BaseSpreadsheet


class QuestionsSpreadsheet(BaseSpreadsheet):

    def __init__(self):
        super(QuestionsSpreadsheet, self).__init__()
        self.hide_column(3) # Type
        self.hide_column(5) # Data Resource Column
        self.hide_column(6) # ID Column

    def get_sheet_name(self):
        return 'Sheet1'

    def get_google_sheet_url(self):
        load_dotenv()
        return os.getenv('QUESTIONS')

    def get_header(self):
        return [
            'EMAIL',
            'JOBS_LINK',
            'TYPE',
            'QUESTION',
            'ID',
            'DATA RESOURCE',
            'ANSWER'
        ]

    def find_answer(self, email:str, job_id: int) -> List[Dict]:
        records = self.data_sheet.get_all_records()
        data = []
        for row in records:
            job_match = str(job_id).lower() in row['JOBS_LINK'].lower()
            email_match = row['EMAIL'].lower() == email.lower()
            if job_match and email_match:
                if row['ANSWER']:
                    data.append({
                        'answer': row['ANSWER'],
                        'datasource': json.loads(row['DATA RESOURCE']),
                        'type': row['TYPE'],
                        'id': row['ID']
                    })
        return data

    def hide_column(self, index):
        requests = [
            {
                'updateDimensionProperties': {
                    'range': {
                        'sheetId': self.data_sheet.id,
                        'dimension': 'COLUMNS',
                        'startIndex': index - 1,
                        'endIndex': index,
                    },
                    'properties': {
                        'hiddenByUser': True
                    },
                    'fields': 'hiddenByUser'
                }
            }
        ]
        self.sh.batch_update({'requests': requests})

    def dropdown_request(self, options, row_index, col_index=0):
        return {
            'setDataValidation': {
                'range': {
                    'sheetId': self.data_sheet.id,
                    'startRowIndex': row_index + 1,
                    'endRowIndex': row_index + 2,
                    'startColumnIndex': col_index + 6,
                    'endColumnIndex': col_index + 7,
                },
                'rule': {
                    'showCustomUi': True,
                    'strict': True,
                    'condition': { 'values': options, 'type': 'ONE_OF_LIST'},
                },
            }
        }

    def generate_dropdown(self, condition: Callable[[dict], Tuple]):
        values = self.data_sheet.get_all_values()[1:]
        requests = []
        for row_index, row in enumerate(values):
            proceed, options = condition(row)
            if proceed: requests.append(self.dropdown_request(options=options, row_index=row_index))
        self.sh.batch_update({"requests": requests})

    def add_job_question(self, email: str, job_url: str, _type: str, question: str, question_id: str, answers: list):
        self.data_sheet.append_row(
            [email, job_url, _type, question, question_id, json.dumps(answers) ,"`"],
            value_input_option='USER_ENTERED')