import json
import os
import time
import requests
import threading

from scripts.spreadsheets import QuestionsSpreadsheet, JobsSpreadsheet
from typing import List, Tuple
from bs4 import BeautifulSoup

from selenium.common.exceptions import NoAlertPresentException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select

from core.browser import Browser
from core.logging import logger

from models import CandidateData
from models.seek import JobSearchResultModel, Job


class SeekAutomation:

    def __init__(self, debug: bool, url: str, email: str, password: str, resume_option_text: str):
        self.session = requests.session()
        self.session.headers.update({
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/104.0.0.0 Safari/537.36'})
        self.url = url
        self.jobs_spreadsheet = JobsSpreadsheet()
        self.questions_spreadsheet = QuestionsSpreadsheet()
        self.email = email
        self.password = password
        self.resume_option_text = resume_option_text
        self.browser = Browser(email=self.email)
        self.applied_jobs = []
        self.debug = debug

    @classmethod
    def from_candidate_data(cls, debug: bool, candidate_data: CandidateData):
        return cls(debug, url=candidate_data.url, email=candidate_data.email, password=candidate_data.password,
                   resume_option_text=candidate_data.resume_option_text)

    def get_jobs(self, page=1) -> Tuple[List[Job], int]:
        response = self.session.get(self.url, params={'page': page})
        logger.info(f"Jobs Page Response : {response.status_code}")
        page = BeautifulSoup(response.text, features='lxml')
        for script in page.select('script'):
            if script.get('data-automation', '') == 'server-state':
                if 'window.SEEK_CONFIG' in str(script.string):
                    data_string = script.string.split('window.SEEK_REDUX_DATA = ')[1].split('window.SEEK_APP_CONFIG')[
                                      0].replace('undefined', 'null').strip()[:-1]
                    data = json.loads(data_string)
                    search_result = JobSearchResultModel.parse_obj(data)
                    total_pages = int(
                        search_result.results.solMetadata.totalJobCount / search_result.results.solMetadata.pageSize)
                    return search_result.results.results.jobs, total_pages

    def apply_to_jobs(self):
        threading.current_thread().name = self.email
        jobs, total_pages = self.get_jobs()
        if total_pages > 1:
            for page in range(2, total_pages + 1):
                jobs_on_next_pages, pages = self.get_jobs(page)
                jobs += jobs_on_next_pages

        if jobs is None or len(jobs) == 0:
            logger.info('No Jobs to apply.')
            return
        self.login()
        logger.info(f'Jobs Applied : {self.applied_jobs}')
        self.applied_jobs = self.jobs_spreadsheet.get_applied_job_list(self.email)

        
        for job in jobs:
            if self.debug:
                job_ids = [
                    61364516, #checkboxes
                    62881879, #radio
                    61411773, #input
                    61854787, #dropdown
                    61436327, #dropdown
                    62881879, #dropdown
                    62841427  #dropdown
                ]
                if job.id in job_ids:
                    self.apply_to_job(job)
            else:
                if job.id not in self.applied_jobs:
                    self.apply_to_job(job)
        self.browser.close()

    def login(self):
        homepage_url = 'https://www.seek.com.au/'
        self.browser.open_url(homepage_url)
        time.sleep(5)
        self.browser.wait_and_click((By.CSS_SELECTOR, '[data-automation="sign-in-register"]'))
        time.sleep(5)
        try:
            email_element = self.browser.driver.find_element(By.ID, 'emailAddress')
            email_element.clear()
            email_element.send_keys(self.email)
            self.browser.wait_and_type((By.ID, 'password'), self.password)
            self.browser.wait_and_click((By.CSS_SELECTOR, '[data-cy="login"]'))
        except NoSuchElementException:
            logger.info('Login Not Required.')

        self.browser.wait_driver.until(
            expected_conditions.url_to_be(
                homepage_url)
        )

    def click_continue(self):
        self.browser.wait_and_click((By.CSS_SELECTOR, '[data-testid="continue-button"]'))

    def failed(self, job: Job, reason: str):
        self.applied_jobs.append(job.id)
        self.jobs_spreadsheet.add_job_data(self.email, job.title, job.get_job_post_link, 'FAILED', reason)

    def passed(self, job: Job):
        self.applied_jobs.append(job.id)
        self.jobs_spreadsheet.add_job_data(self.email, job.title, job.get_job_post_link, 'SUCCESS')

    def get_job_url(self, job: Job) -> str:
        return f"https://www.seek.com.au/job/{job.id}/apply"
    
    def apply_to_job(self, job: Job):
        logger.info(f'Opening URL : {job.url}')
        skip = self.apply_step_one(job)
        if not skip:
            self.apply_step_two()
            self.apply_step_three(job)
            self.apply_step_four()
            self.apply_step_five()
            self.apply_step_six(job)
        else:
            self.browser.driver.back()

    def apply_step_one(self, job: Job) -> bool:
        self.browser.open_url(self.get_job_url(job))
        try:
            self.browser.driver.switch_to.alert.accept()
            self.browser.driver.switch_to.alert.dismiss()
        except NoAlertPresentException:
            pass

        time.sleep(8)
        if 'seek.com.au' not in self.browser.driver.current_url:
            logger.info("External Job")
            self.failed(job, 'External')
            return True
        return False

    def apply_step_two(self):
        resume_select = Select(self.browser.wait_for_visibility((By.ID, 'selectedResume')))
        resume_select.select_by_visible_text(self.resume_option_text)
        # Do not include cover letter
        self.browser.driver.find_element(By.CSS_SELECTOR, '[data-testid="dontIncludecoverLetter"]').click()
        self.click_continue()
        time.sleep(5)
    
    def apply_step_three(self, job: Job):
        raise NotImplemented

    def apply_step_four(self):
        if 'Update SEEK Profile' in self.browser.get_bs4_page().title.text:
            self.click_continue()
            time.sleep(5)

    def apply_step_five(self):
        if 'Review and submit' in self.browser.get_bs4_page().title.text:
            self.browser.wait_and_click((By.CSS_SELECTOR, '[data-testid="review-submit-application"]'))
            time.sleep(5)

    def apply_step_six(self, job: Job):
        if 'Application sent' in self.browser.get_bs4_page().title.text:
            self.passed(job)
            logger.info("Applied Successfully.")
