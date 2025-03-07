import extract_msg
import re
from file_processing.errors import FileProcessingFailedError
from file_processing.file_processor_strategy import FileProcessorStrategy

class MsgFileProcessor(FileProcessorStrategy):
    """
    Processor for Outlook MSG files, building a strictly linear thread:
      oldest -> next -> ... -> newest
    """

    def __init__(self, file_path: str, open_file: bool = True) -> None:
        super().__init__(file_path, open_file)
        self.metadata = {'message': 'File was not opened'} if not open_file else {}

    def split_email_thread(self, body_text: str) -> list[str]:
        """
        Splits the raw body into blocks based on lines that begin with 'From:'.
        """
        pattern = r"(?m)^(?=From:\s)"
        parts = re.split(pattern, body_text or "")
        # Strip whitespace and drop empties
        return [p.strip() for p in parts if p.strip()]

    def parse_email_block(self, block_text: str) -> dict | None:
        """
        Relaxed parsing:
         - Requires at least a line starting with 'From:' to consider it a valid older email.
         - Optionally captures Sent: or Date:, To:, Subject:, storing the rest in 'body'.
         - Returns None if no 'From:' line is found.
        """
        from_match = re.search(r"(?im)^From:\s*(.*)$", block_text)
        if not from_match:
            return None  # Not an older email

        sender = from_match.group(1).strip()

        # Try "Sent:" first, then fallback to "Date:"
        sent_match = re.search(r"(?im)^Sent(?: on)?:\s*(.*)$", block_text)
        timestamp = sent_match.group(1).strip() if sent_match else None
        if not timestamp:
            date_match = re.search(r"(?im)^Date:\s*(.*)$", block_text)
            timestamp = date_match.group(1).strip() if date_match else None

        # 'To:' is optional
        to_match = re.search(r"(?im)^To:\s*(.*)$", block_text)
        recipients_raw = to_match.group(1).strip() if to_match else ""
        recipients = [r.strip() for r in re.split(r"[;,]", recipients_raw) if r.strip()] if recipients_raw else []

        # 'Subject:' is optional
        subject_match = re.search(r"(?im)^Subject:\s*(.*)$", block_text)
        subject = subject_match.group(1).strip() if subject_match else None

        # Remove recognized lines from the text for the 'body'
        pattern_remove = r"(?im)^(From|Sent(?: on)?|Date|To|Subject):.*?$"
        cleaned_body = re.sub(pattern_remove, "", block_text).strip()

        return {
            "subject": subject,
            "sender": sender,
            "recipients": recipients,
            "timestamp": timestamp,
            "body": cleaned_body,
            "reply": None
        }

    def build_linear_chain(self, emails: list[dict]) -> dict | None:
        """
        Chain emails linearly: each email's 'reply' references the next.
        'emails' should be in chronological order: [oldest, 2nd, ..., newest].
        Returns the oldest (head).
        """
        if not emails:
            return None
        head = emails[0]
        current = head
        for nxt in emails[1:]:
            current["reply"] = nxt
            current = nxt
        return head

    def parse_msg(self) -> dict:
        """
        1) Splits the raw .body into blocks on 'From:' lines.
        2) Parses each block in *reverse* order so the earliest is first.
        3) Builds a single chain from oldest -> newest.
        4) Optionally merges leftover text or appends a "main" .msg email if desired.
        """
        msg = extract_msg.Message(self.file_path)
        raw_body = msg.body or ""

        # Split on 'From:'
        blocks = self.split_email_thread(raw_body)
        if not blocks:
            # No 'From:' lines => everything is one "main" message
            only_node = {
                "subject": msg.subject,
                "sender": msg.sender,
                "recipients": [r.strip() for r in msg.to.split(";")] if msg.to else [],
                "timestamp": msg.date.isoformat() if msg.date else None,
                "body": raw_body,
                "reply": None
            }
            msg.close()
            return only_node

        # Step 1: parse each block
        # The raw text often has the newest email at the top, so reverse blocks to read from oldest to newest
        reversed_blocks = list(reversed(blocks))

        parsed_emails = []
        leftover_chunks = []

        for blk in reversed_blocks:
            parsed = self.parse_email_block(blk)
            if parsed:
                parsed_emails.append(parsed)
            else:
                leftover_chunks.append(blk)

        # Step 2: Build the chain (oldest->...->newest) from these parsed emails
        chain_head = self.build_linear_chain(parsed_emails)

        # Step 3: If there is leftover text, or if we want an explicit "main email" node
        #         with the actual .msg metadata, create it and append at the end.
        leftover_body = "\n\n".join(leftover_chunks).strip()
        # Possibly you'd only do this if you *expect* the .msg's top-level email to appear:
        main_node = {
            "subject": msg.subject,
            "sender": msg.sender,
            "recipients": [r.strip() for r in msg.to.split(";")] if msg.to else [],
            "timestamp": msg.date.isoformat() if msg.date else None,
            "body": leftover_body or "",  # or raw_body if you want to unify everything
            "reply": None
        }

        # If leftover_body is empty, you could skip the main node, but let's assume we keep it:
        if chain_head:
            # walk to the last node
            current = chain_head
            while current["reply"] is not None:
                current = current["reply"]
            current["reply"] = main_node
            final_thread = chain_head
        else:
            # no older emails => main node is entire thread
            final_thread = main_node

        msg.close()
        return final_thread

    def process(self) -> None:
        """
        Reads the MSG file, extracts top-level metadata, and builds the linear thread.
        """
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"Processing file: {self.file_path}")

        if not self.open_file:
            return

        try:
            msg = extract_msg.Message(self.file_path)
            self.metadata["text"] = msg.body
            self.metadata["subject"] = msg.subject
            self.metadata["date"] = msg.date
            self.metadata["sender"] = msg.sender
            self.metadata["recipients"] = [r.email for r in msg.recipients if r.email]
            msg.close()

            # Now parse entire chain in correct chronological order
            self.metadata["thread"] = self.parse_msg()

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
