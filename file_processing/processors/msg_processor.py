import extract_msg
from file_processing.errors import FileProcessingFailedError
from file_processing.file_processor_strategy import FileProcessorStrategy

class MsgFileProcessor(FileProcessorStrategy):
    """
    Processor for handling Outlook MSG files, extracting metadata such as message body, subject,
    date, and sender.

    Attributes:
        metadata (dict): Contains metadata fields such as 'text', 'subject', 'date', and 'sender'
                         if the file is opened.
    """

    def __init__(self, file_path: str, open_file: bool = True) -> None:
        """
        Initializes the MsgFileProcessor with the specified file path.

        Args:
            file_path (str): Path to the MSG file to process.
            open_file (bool): Indicates whether to open and process the file immediately.

        Sets:
            metadata (dict): Populated with a message if `open_file` is False, otherwise initialized as empty.
        """
        super().__init__(file_path, open_file)
        self.metadata = {'message': 'File was not opened'} if not open_file else {}

    def process(self) -> None:
        """
        Extracts metadata from the MSG file, including text content, subject, date, and sender.

        Raises:
            FileProcessingFailedError: If an error occurs during MSG file processing.
        """
        if not self.open_file:
            return

        try:
            # Open and read the MSG file
            msg = extract_msg.Message(self.file_path)
            self.metadata.update({
                'text': msg.body,
                'subject': msg.subject,
                'date': msg.date,
                'sender': msg.sender,
            })
            msg.close()
        except Exception as e:
            raise FileProcessingFailedError(
                f"Error encountered while processing: {e}"
            )

    def save(self, output_path: str = None) -> None:
        """
        Saves the MSG file to the specified output path.

        Args:
            output_path (str): Path to save the MSG file. If None, overwrites the original file.

        Raises:
            FileProcessingFailedError: If an error occurs while saving the MSG file.
        """
        try:
            output_path = output_path or self.file_path
            msg_file = extract_msg.Message(self.file_path)
            msg_file.export(path=output_path)
            msg_file.close()
        except Exception as e:
            raise FileProcessingFailedError(
                f"Error encountered while saving: {e}"
            )
