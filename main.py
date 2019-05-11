"""
Author: Mohit Musaddi
Status: Development
Date: 15/04/2019
"""

from scrap.web import Webpage
from scrap.table import Table

def run():
    court = Webpage()
    court.process()
    # print(court.table_html)
    table = Table(court.table_html)
    result_file_path = 'output/'
    table.process(result_file_path)

if __name__ == '__main__':
    run()