from core.seek import SeekAutomation
from scrapers import SeekScraper
from models.seek import Job
from typing import Tuple
import json


def condition(row:dict) -> Tuple[bool,list]:
    if row[2] == 'SingleChoiceQuestion' or row[2] == 'MultipleChoiceQuestion':
        data = json.loads(row[5])
        return True, [ {'userEnteredValue': str(option['text']) } for option in  data]
    return False, []


class Submit(SeekAutomation):
                   
    def apply_step_three(self, job: Job):
        if 'employer questions' in self.browser.get_bs4_page().title.text:
            self.failed(job, 'Requires Question & Answers')
            data = SeekScraper.get_questions_answers(job.id)
            for question in data['questions']:
                self.questions_spreadsheet.add_job_question(
                    self.email,
                    data['job_url'],
                    question['__typename'],
                    question['text'],
                    question['id'],
                    question.get('options', [])
                )
            """
                After writing all the questions, it will be followed by
                generation of dropdown to present the answers nicely.
            """
            self.questions_spreadsheet.generate_dropdown(condition)
