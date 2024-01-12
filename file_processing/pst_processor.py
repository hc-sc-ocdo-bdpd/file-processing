# import os
# import time
# import shutil
# import win32com.client
# from pathlib import Path
# from datetime import datetime
# from errors import FileProcessingFailedError
# from file_processor_strategy import FileProcessorStrategy


# class PstFileProcessor(FileProcessorStrategy):
#     def __init__(self, file_path: str, open_file: bool = True) -> None:
#         super().__init__(file_path, open_file)
#         self.metadata = {
#             'message': 'File was not opened'} if not open_file else {}

#     def process(self) -> None:
#         if not self.open_file:
#             return

#         try:
#             Outlook = win32com.client.Dispatch(
#                 "Outlook.Application").GetNamespace("MAPI")
#             path = os.path.abspath(self.file_path)
#             path = path[0].upper() + path[1:]
#             Outlook.AddStore(path)
#             PSTFolderObj = self._find_pst_folder(Outlook, path)
#             num_files, emails, file_names = self._count_files(PSTFolderObj)

#             self.metadata.update({"num_folders": len(PSTFolderObj.Folders)})
#             self.metadata.update({"num_files": num_files})
#             self.metadata.update({"file_types": {"msg": num_files}})
#             self.metadata.update({"file_names": file_names})
#             self.metadata.update({"emails": emails})
#             Outlook.RemoveStore(PSTFolderObj)

#         except Exception as e:
#             raise FileProcessingFailedError(
#                 f"Error encountered while processing {self.file_path}: {e}")

#     def _find_pst_folder(self, OutlookObj, pst_filepath):
#         for Store in OutlookObj.Stores:
#             if Store.IsDataFileStore and Store.FilePath == pst_filepath:
#                 return Store.GetRootFolder()
#         return None

#     def _count_files(self, FolderObj):
#         num_files = 0
#         emails, file_names = [], []

#         for ChildFolder in FolderObj.Folders:
#             files, emails, file_names = self._count_files(ChildFolder)
#             num_files += files

#         num_files += len(FolderObj.Items)
#         for item in FolderObj.Items:
#             dt = datetime(item.SentOn.year, item.SentOn.month, item.SentOn.day, item.SentOn.hour,
#                 item.SentOn.minute, item.SentOn.second)
#             emails.append(item.Subject)
#             file_names.append(f'{int(dt.timestamp() * 1000)}.msg')

#         return num_files, emails, file_names

#     def _extract_files(self, FolderObj, output_dir):
#         for ChildFolder in FolderObj.Folders:
#             self._extract_files(ChildFolder, output_dir)

#         for item in FolderObj.Items:
#             dt = datetime(item.SentOn.year, item.SentOn.month, item.SentOn.day, item.SentOn.hour,
#                           item.SentOn.minute, item.SentOn.second)
#             try:
#                 item.SaveAs(os.path.join(
#                     output_dir, f'{int(dt.timestamp() * 1000)}.msg'), 3)
#             except Exception as ex:
#                 raise FileProcessingFailedError(
#                     f"Error encountered while extracting {f'{int(dt.timestamp() * 1000)}.msg'}: {ex}")

#     def extract(self, output_dir: str = None) -> None:
#         try:

#             path = os.path.abspath(self.file_path)
#             path = path[0].upper() + path[1:]

#             if not output_dir:
#                 output_dir = os.path.splitext(path)[0]

#             Path(output_dir).mkdir(parents=True, exist_ok=True)

#             Outlook = win32com.client.Dispatch(
#                 "Outlook.Application").GetNamespace("MAPI")
#             Outlook.AddStore(path)
#             PSTFolderObj = self._find_pst_folder(Outlook, path)
#             self._extract_files(PSTFolderObj, output_dir)
#             Outlook.RemoveStore(PSTFolderObj)

#         except Exception as e:
#             raise FileProcessingFailedError(
#                 f"Error encountered while extracting {self.file_path}: {e}")

#     def save(self, output_path: str = None) -> None:
#         try:
#             output_path = output_path or str(self.file_path)
#             time.sleep(8)  # wait for Outlook to finish processing in the background
#             shutil.copy2(self.file_path, output_path)
#         except Exception as e:
#             raise FileProcessingFailedError(
#                 f"Error encountered while saving {self.file_path}: {e}")
