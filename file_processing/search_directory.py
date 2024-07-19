import os
from file_processing import Directory

class SearchDirectory:
    def __init__(self, folder_path: str):
        self.folder_path = folder_path

    def get_report(self, directory_path: str) -> None:
        directory = Directory(directory_path)
        directory.generate_report(
            report_file = os.path.join(self.folder_path,"report.csv"),
            split_metadata=True,
            include_text=True,
        )