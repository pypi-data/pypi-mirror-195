import os
from dotenv import load_dotenv
from core.googlesheet import BaseSpreadsheet
from models import CandidateData


class CandidateSpreadsheet(BaseSpreadsheet):
    def __init__(self):
        super(CandidateSpreadsheet, self).__init__()

    def get_sheet_name(self):
        return 'Sheet1'

    def get_google_sheet_url(self):
        load_dotenv()
        return os.getenv('CANDIDATES')

    def get_header(self):
        return [
            'EMAIL',
            'PASSWORD',
            'RESUME_OPTION_TEXT',
            'JOBS_LINK',
            'AUTOMATION_STATUS',
            'START'
        ]

    def find_candidate_by_email(self, email: str) -> CandidateData:
        for row in self.data_sheet.get_all_records():
            if row['EMAIL'].lower() == email.lower():
                return CandidateData.parse_obj(row)

    def start_automation(self) -> bool:
        return self.data_sheet.cell(row=1, col=6).value.lower() == 'start'
