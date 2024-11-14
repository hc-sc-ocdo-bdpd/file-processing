import ast
import shutil
from file_processing.errors import FileProcessingFailedError
from file_processing.file_processor_strategy import FileProcessorStrategy

class PyFileProcessor(FileProcessorStrategy):
    """
    Processor for handling Python (.py) files, extracting metadata such as line count,
    function count, class count, imports, docstrings, and full text content.

    Attributes:
        metadata (dict): Contains metadata fields such as 'num_lines', 'num_functions',
                         'num_classes', 'imports', 'docstrings', and 'text' if the file is opened.
    """

    def __init__(self, file_path: str, open_file: bool = True) -> None:
        """
        Initializes the PyFileProcessor with the specified file path.

        Args:
            file_path (str): Path to the Python file to process.
            open_file (bool): Indicates whether to open and process the file immediately.

        Sets:
            metadata (dict): Populated with a message if `open_file` is False, otherwise initialized with default values.
        """
        super().__init__(file_path, open_file)
        self.metadata = {'message': 'File was not opened'} if not open_file else self._default_metadata()

    def _default_metadata(self) -> dict:
        """
        Returns default metadata for an unopened Python file.

        Returns:
            dict: Default metadata with 'num_lines', 'num_functions', 'num_classes',
                  'imports', 'docstrings', and 'text' fields.
        """
        return {
            'num_lines': 0,
            'num_functions': 0,
            'num_classes': 0,
            'imports': [],
            'docstrings': [],
            'text': None
        }

    def process(self) -> None:
        """
        Extracts metadata from the Python file, including line count, function count,
        class count, imports, docstrings, and full text content.

        Raises:
            FileProcessingFailedError: If an error occurs during Python file processing.
        """
        if not self.open_file:
            return

        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                self.metadata['num_lines'] = len(content.splitlines())
                self.metadata['text'] = content
                ast_tree = ast.parse(content)
                self._extract_metadata(ast_tree)
        except Exception as e:
            raise FileProcessingFailedError(
                f"Error encountered while processing {self.file_path}: {e}"
            )

    def _extract_metadata(self, ast_tree) -> None:
        """
        Extracts metadata from the abstract syntax tree (AST) of the Python file,
        counting functions, classes, and collecting imports and docstrings.

        Args:
            ast_tree (AST): The abstract syntax tree of the Python file content.
        """
        for node in ast.walk(ast_tree):
            if isinstance(node, ast.FunctionDef):
                self.metadata['num_functions'] += 1
                if node.body and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Str):
                    self.metadata['docstrings'].append(node.body[0].value.s)
            elif isinstance(node, ast.ClassDef):
                self.metadata['num_classes'] += 1
                if node.body and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Str):
                    self.metadata['docstrings'].append(node.body[0].value.s)
            elif isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                self.metadata['imports'].append(ast.unparse(node))

    def save(self, output_path: str = None) -> None:
        """
        Saves the Python file to the specified output path.

        Args:
            output_path (str): Path to save the Python file. If None, overwrites the original file.

        Raises:
            FileProcessingFailedError: If an error occurs while saving the Python file.
        """
        if output_path is None:
            output_path = self.file_path
        try:
            shutil.copy2(self.file_path, output_path)
        except Exception as e:
            raise FileProcessingFailedError(
                f"Error encountered while saving to {output_path}: {e}"
            )
