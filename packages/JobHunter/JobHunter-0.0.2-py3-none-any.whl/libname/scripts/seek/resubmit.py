import time
from gspread import Cell

from models import CandidateData
from models.seek import Job

from core.seek import SeekAutomation
from core.logging import logger

from selenium.webdriver.common.by import By
from selenium.common.exceptions import UnexpectedTagNameException
from selenium.webdriver.support.select import Select


class ReSubmit(SeekAutomation):

    def __init__(self, *args, **kwargs):
        self.job_index = kwargs.pop('job_index')
        super().__init__(*args, **kwargs)
    
    @classmethod
    def from_candidate_data(cls, debug: bool, job_index: int, candidate_data: CandidateData):
        return cls(debug, url=candidate_data.url, email=candidate_data.email, password=candidate_data.password,
                   resume_option_text=candidate_data.resume_option_text, job_index=job_index)

    def answer_checkbox_radio_question(self, answer):
        source = [ans['id'] for ans in answer['datasource'] if ans['text'].lower() == answer['answer'].lower()]
        answer_id = f"{source[0]}{answer['id']}"
        self.browser.driver.find_element(By.CSS_SELECTOR, f'[data-testid="{answer_id}"]').click()
        
    def answer_text_question(self, answer):
        question_id = f"question-{answer['id']}"
        print(question_id)
        input_element = self.browser.driver.find_element(By.ID, question_id)
        input_element.send_keys(answer['answer'])
    
    def answer_dropdown_select_question(self, answer):
        question_id = f"question-{answer['id']}"
        try:
            answer_select = Select(self.browser.wait_for_visibility((By.ID, question_id)))
            answer_select.select_by_visible_text(answer['answer'])
        except UnexpectedTagNameException:
            self.answer_checkbox_radio_question(answer)
            
    def apply_step_three(self, job: Job):
        if 'employer questions' in self.browser.get_bs4_page().title.text:
            answers = self.questions_spreadsheet.find_answer(self.email, job.id)
            for answer in answers:
                if answer['answer'] == '`': return
                if answer['type'] == 'FreeTextQuestion': self.answer_text_question(answer)
                if answer['type'] == 'MultipleChoiceQuestion': self.answer_checkbox_radio_question(answer)
                if answer['type'] == 'SingleChoiceQuestion': self.answer_dropdown_select_question(answer)
            self.click_continue()
            time.sleep(5)
    
    def apply_step_six(self, job: Job):
        if 'Application sent' in self.browser.get_bs4_page().title.text:
            self.jobs_spreadsheet.data_sheet.update_cells([Cell(row=self.job_index,col=4, value='SUCCESS')])
            logger.info("Applied Successfully.")