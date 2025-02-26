import extract_msg
import re
from file_processing.errors import FileProcessingFailedError
from file_processing.file_processor_strategy import FileProcessorStrategy

class MsgFileProcessor(FileProcessorStrategy):
    """
    Processor for handling Outlook MSG files, extracting metadata such as message body, subject,
    date, sender, and constructing a strictly linear email thread (each email has a single reply).
    """

    def __init__(self, file_path: str, open_file: bool = True) -> None:
        super().__init__(file_path, open_file)
        self.metadata = {'message': 'File was not opened'} if not open_file else {}

    def split_email_thread(self, body_text: str) -> list[str]:
        # Split on lines beginning with 'From:'
        pattern = r"(?m)^(?=From:\s)"
        parts = re.split(pattern, body_text or "")
        return [part.strip() for part in parts if part.strip()]

    def parse_email_block(self, email_text: str) -> dict:
        """
        Return a dict with a single 'reply' child (None by default).
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
            recipients_raw = match.group(3).strip()
            recipients = [r.strip() for r in re.split(r"[;,]", recipients_raw) if r.strip()]
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
            "reply": None  # Single next email, if any
        }

    def build_linear_chain(self, parsed_emails: list[dict]) -> dict:
        """
        Build a strictly linear chain: each email has at most one child in 'reply'.
        Returns the oldest email (head of the chain).
        """
        if not parsed_emails:
            return {}

        head = parsed_emails[0]
        current = head
        for email in parsed_emails[1:]:
            current["reply"] = email
            current = email
        return head

    def parse_msg(self) -> dict:
        """
        Parse the .msg file and construct a strictly linear thread.
        The newest email overrides the last parsed email's metadata.
        """
        msg = extract_msg.Message(self.file_path)
        raw_body = msg.body or ""

        # Split body into chunks
        email_blocks = self.split_email_thread(raw_body)
        parsed_emails = [self.parse_email_block(block) for block in email_blocks]

        if parsed_emails:
            # The last block is actually the newest email in the chain;
            # overwrite it with the real MSG metadata.
            newest_email = parsed_emails[-1]
            newest_email["subject"] = msg.subject
            newest_email["sender"] = msg.sender
            if msg.to:
                newest_email["recipients"] = [r.strip() for r in msg.to.split(";")]
            if msg.date:
                newest_email["timestamp"] = msg.date.isoformat()

        # Build the chain from oldest to newest
        final_thread = self.build_linear_chain(parsed_emails)

        msg.close()
        return final_thread

    def process(self) -> None:
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"Processing file: {self.file_path}")

        if not self.open_file:
            return

        try:
            msg = extract_msg.Message(self.file_path)
            self.metadata.update({
                'text': msg.body,
                'subject': msg.subject,
                'date': msg.date,
                'sender': msg.sender,
            })
            # Construct the linear thread
            self.metadata['thread'] = self.parse_msg()
            msg.close()

        except Exception as e:
            raise FileProcessingFailedError(
                f"Error encountered while processing: {e}"
            )

    def save(self, output_path: str = None) -> None:
        try:
            output_path = output_path or self.file_path
            msg_file = extract_msg.Message(self.file_path)
            msg_file.export(path=output_path)
            msg_file.close()
        except Exception as e:
            raise FileProcessingFailedError(
                f"Error encountered while saving: {e}"
            )
