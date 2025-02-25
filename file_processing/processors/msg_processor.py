import extract_msg
import os
import re
from file_processing.errors import FileProcessingFailedError
from file_processing.file_processor_strategy import FileProcessorStrategy

class MsgFileProcessor(FileProcessorStrategy):
    """
    Processor for handling Outlook MSG files, extracting metadata such as message body, subject,
    date, sender, and constructing a nested email thread.
    """

    def __init__(self, file_path: str, open_file: bool = True) -> None:
        """
        Initializes the MsgFileProcessor with the specified file path.

        Args:
            file_path (str): Path to the MSG file to process.
            open_file (bool): Indicates whether to open and process the file immediately.
        """
        super().__init__(file_path, open_file)
        self.metadata = {'message': 'File was not opened'} if not open_file else {}

    def split_email_thread(self, body_text) -> list[str]:
        """
        Splits the full email body into parts based on lines starting with "From:".
        Outlook typically uses "From:" to indicate the beginning of a quoted message.
        """
        pattern = r"(?m)^(?=From:\s)"
        parts = re.split(pattern, body_text)
        return [part.strip() for part in parts if part.strip()]

    def parse_email_block(self, email_text) -> dict:
        """
        Parses an email block, extracting metadata like sender, timestamp, recipients, and subject.
        """
        metadata_regex = (
            r"From:\s*(.+?)\s*\r?\n"
            r"Sent(?: on)?:\s*(.+?)\s*\r?\n"
            r"To:\s*(.+?)\s*\r?\n"
            r"Subject:\s*(.+?)(?:\r?\n|$)"
        )
        match = re.search(metadata_regex, email_text, flags=re.IGNORECASE | re.DOTALL)
        if match:
            sender = match.group(1).strip()
            timestamp = match.group(2).strip()
            recipients = [r.strip() for r in match.group(3).split(";") if r.strip()]
            subject = match.group(4).strip()
            body = email_text[match.end():].strip()
        else:
            sender = None
            timestamp = None
            recipients = []
            subject = None
            body = email_text
        return {
            "subject": subject,
            "sender": sender,
            "recipients": recipients,
            "timestamp": timestamp,
            "body": body,
            "replies": []
        }

    def build_nested_thread(self, email_parts) -> dict:
        """
        Constructs a nested email thread from a list of parsed email parts.
        """
        parsed_emails = [self.parse_email_block(part) for part in email_parts]
        chronological = list(reversed(parsed_emails))
        root = chronological[0]
        current = root
        for email in chronological[1:]:
            current["replies"] = [email]
            current = email
        return root

    def parse_msg(self) -> dict:
        """
        Parses the .msg file and constructs the email thread.
        """
        msg = extract_msg.Message(self.file_path)
        email_parts = self.split_email_thread(msg.body)

        top_email = {
            "subject": msg.subject,
            "sender": msg.sender,
            "recipients": msg.to.split("; ") if msg.to else [],
            "timestamp": msg.date.isoformat() if msg.date else None,
            "body": email_parts[0] if email_parts else msg.body,
            "replies": []
        }

        if len(email_parts) > 1:
            forwarded_chain = self.build_nested_thread(email_parts[1:])
            forwarded_chain["replies"].append(top_email)
            final_thread = forwarded_chain
        else:
            final_thread = top_email

        return final_thread

    def process(self) -> None:
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"Processing file: {self.file_path}")
        """
        Extracts metadata from the MSG file, including text content, subject, date, sender,
        and constructs the email thread.
        """
        if not self.open_file:
            return

        try:
            msg = extract_msg.Message(self.file_path)
            self.metadata.update({
                'text': msg.body,
                'subject': msg.subject,
                'date': msg.date,
                'sender': msg.sender,
                'thread': self.parse_msg()
            })
            msg.close()
        except Exception as e:
            raise FileProcessingFailedError(
                f"Error encountered while processing: {e}"
            )

    def save(self, output_path: str = None) -> None:
        """
        Saves the MSG file to the specified output path.
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
