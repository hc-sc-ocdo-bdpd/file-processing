import chardet  
import re  
from file_processing.errors import FileProcessingFailedError  
from file_processing.file_processor_strategy import FileProcessorStrategy  
  
class CFileProcessor(FileProcessorStrategy):  
    """  
    Processor for handling C (.c) source files, extracting useful metadata.  
  
    Attributes:  
        metadata (dict): Contains extracted metadata such as:  
            - text: full file text  
            - encoding: detected file encoding  
            - num_lines: total number of lines  
            - num_blank_lines: number of blank lines  
            - num_comment_lines: number of comment lines  
            - num_code_lines: number of code lines  
            - num_includes: number of '#include' statements  
            - num_defines: number of '#define' statements  
            - num_functions: number of function definitions  
            - num_todos: number of "TODO" comments  
    """  
  
    def __init__(self, file_path: str, open_file: bool = True) -> None:  
        super().__init__(file_path, open_file)  
        self.metadata = {'message': 'File was not opened'} if not open_file else {}  
  
    def process(self) -> None:  
        if not self.open_file:  
            return  
        try:  
            with open(self.file_path, 'rb') as f:  
                raw_data = f.read()  
                encoding = chardet.detect(raw_data)['encoding']  
                text = raw_data.decode(encoding)  
  
            lines = text.splitlines()  
            num_lines = len(lines)  
            num_blank_lines = sum(1 for line in lines if line.strip() == '')  
            num_comment_lines = sum(1 for line in lines if line.strip().startswith(("//", "/*", "*")))  
            num_code_lines = num_lines - num_blank_lines - num_comment_lines  
  
            num_includes = len(re.findall(r'^\s*#include', text, re.MULTILINE))  
            num_defines = len(re.findall(r'^\s*#define', text, re.MULTILINE))  
            num_functions = len(re.findall(r'^[\w\s\*]+?\s+\**\w+\s*\([^\)]*\)\s*\{', text, re.MULTILINE))  
            num_todos = len(re.findall(r'TODO', text))  
  
            self.metadata.update({  
                'text': text,  
                'encoding': encoding,  
                'num_lines': num_lines,  
                'num_blank_lines': num_blank_lines,  
                'num_comment_lines': num_comment_lines,  
                'num_code_lines': num_code_lines,  
                'num_includes': num_includes,  
                'num_defines': num_defines,  
                'num_functions': num_functions,  
                'num_todos': num_todos  
            })  
  
        except Exception as e:  
            raise FileProcessingFailedError(  
                f"Error processing {self.file_path}: {e}"  
            )  
  
    def save(self, output_path: str = None) -> None:  
        try:  
            save_path = output_path or self.file_path  
            with open(save_path, 'w', encoding=self.metadata['encoding'], newline='\n') as f:  
                f.write(self.metadata['text'])  
        except Exception as e:  
            raise FileProcessingFailedError(  
                f"Error saving file {self.file_path} to {save_path}: {e}"  
            )  