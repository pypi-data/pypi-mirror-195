import os
from dotenv import load_dotenv
from datetime import datetime
from typing import List, Dict
from core.googlesheet import BaseSpreadsheet


class JobsSpreadsheet(BaseSpreadsheet):
  
    def __init__(self):
        super(JobsSpreadsheet, self).__init__()

    def get_sheet_name(self):
        return 'Sheet1'

    def get_google_sheet_url(self):
        load_dotenv()
        return os.getenv('JOBS')

    def get_header(self):
        return [
            'Email',
            'Job Title',
            'Job URL',
            'Application Status',
            'Applied On',
            'Reason (If not successfull)',
            'Phone Number',
            'Name'
        ]

    def update_job_data(self, email: str, job_title: str, job_url: str, status: str, error: str = None):
        pass

    def add_job_data(self, email: str, job_title: str, job_url: str, status: str, error: str = None):
        self.data_sheet.append_row(
            [email, job_title, job_url, status, str(datetime.utcnow()), error],
            value_input_option='USER_ENTERED')

    def get_applied_job_list(self, email, filter_status='') -> List[int]:
        all_records = self.data_sheet.get_all_records()
        self.applied_job_list = []
        for record in all_records:
            if str(record['Email']).strip().lower() == str(email).strip().lower():
                job_id = record['Job URL'].split('job/')[1].split('/')[0]
                self.applied_job_list.append(int(job_id))
        return self.applied_job_list
