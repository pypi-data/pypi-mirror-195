import sys

from models import CandidateData
from models.seek import Job

from scripts.spreadsheets import CandidateSpreadsheet, JobsSpreadsheet
from scripts.seek.submit import Submit
from scripts.seek.resubmit import ReSubmit

import argparse

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--test", help="Set 'True' if you want to use testing jobs", type=bool, default=False)
    parser.add_argument("--version", action="version", version='%(prog)s - Version 1.0')
    args = parser.parse_args()
    return args


args = parseArgs()
job_records = JobsSpreadsheet().get_all_records()
for row_index, row in enumerate(job_records):
    if row['Application Status'] == 'FAILED':
        candidate_data_obj = CandidateSpreadsheet().find_candidate_by_email(row['Email'])
        seek_automation = ReSubmit.from_candidate_data(row_index + 2, candidate_data_obj)
        job = Job(id=int(row['Job URL'].split('/job/')[-1]))        
        seek_automation.apply_to_job(job)
        seek_automation.browser.close()

candidate_records = CandidateSpreadsheet().get_all_records()
for candidate_data in candidate_records:
    candidate_data_obj = CandidateData.parse_obj(candidate_data)
    seek_automation = Submit.from_candidate_data(args.test, candidate_data_obj)
    seek_automation.apply_to_jobs()

  
# import sys, os
# frozen = 'not'
# if getattr(sys, 'frozen', False):
#     # we are running in a bundle
#     frozen = 'ever so'
#     bundle_dir = sys._MEIPASS
# else:
#     # we are running in a normal Python environment
#     bundle_dir = os.path.dirname(os.path.abspath(__file__))
# print( 'we are',frozen,'frozen')
# print( 'bundle dir is', bundle_dir )
# print( 'sys.argv[0] is', sys.argv[0] )
# print( 'sys.argv[1] is', sys.argv[1] )
# print( 'sys.executable is', sys.executable )
# print( 'os.getcwd is', os.getcwd() )