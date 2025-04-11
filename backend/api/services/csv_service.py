import os

class CsvService: 
    def __init__(self):
        self.CSV_UPLOAD_FOLDER = 'src/csv/csvs'

        CSV_UPLOAD_FOLDER = 'src/csv/CSVs'
        os.makedirs(CSV_UPLOAD_FOLDER)
    