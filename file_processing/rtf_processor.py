from file_processor_strategy import FileProcessorStrategy
from striprtf.striprtf import rtf_to_text

class RtfFileProcessor(FileProcessorStrategy):
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.metadata = {}

    def process(self) -> None:
        self.metadata.update({"rtf_text": rtf_to_text(self.file_path)})
        #rtf_text = self.file_path
        #text = rtf_to_text(rtf_text)