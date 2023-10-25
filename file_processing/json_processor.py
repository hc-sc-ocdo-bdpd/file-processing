from file_processor_strategy import FileProcessorStrategy
import json
import chardet
from json.decoder import JSONDecodeError
from errors import FileProcessingFailedError

class JsonFileProcessor(FileProcessorStrategy):
   def __init__(self, file_path: str) -> None:
       super().__init__(file_path)
       self.metadata = {}

   def process(self) -> None:
       try:
           encoding = chardet.detect(open(self.file_path, 'rb').read())['encoding']
           with open(self.file_path, 'r', encoding=encoding) as f:
               try:
                   data = json.load(f)
                   text = json.dumps(data)
                   num_objects = len(data)
                   num_keys = 0
                   empty_values = 0
                   for obj in data:
                       num_keys += len(obj.keys())
                       for key in obj.keys():
                           if obj[key] == '':
                               empty_values += 1
               except JSONDecodeError:
                   text = f.read()
                   num_objects = 0
                   num_keys = 0
                   empty_values = 0
               self.metadata.update({
                   'text': text,
                   'encoding': encoding,
                   'num_objects': num_objects,
                   'num_keys': num_keys,
                   'empty_values': empty_values,
               })
       except Exception as e:
           raise FileProcessingFailedError(f"Error encountered while processing {self.file_path}: {e}")
  

   def save(self, output_path: str = None) -> None:
       try:
           save_path = output_path or self.file_path
           with open(save_path, 'w', encoding = self.metadata['encoding']) as f:
               json.dump(self.metadata['text'], f)
       except Exception as e:
           raise FileProcessingFailedError(f"Error encountered while saving file {self.file_path} to {save_path}: {e}")