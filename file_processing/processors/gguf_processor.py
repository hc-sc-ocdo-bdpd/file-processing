import struct
from file_processing.file_processor_strategy import FileProcessorStrategy
from file_processing.errors import FileProcessingFailedError


class GgufFileProcessor(FileProcessorStrategy):
    GGUF_MAGIC_NUMBER = b"GGUF"
    VALUE_FORMATS = {
        0: "B",  # UINT8
        1: "b",  # INT8
        2: "H",  # UINT16
        3: "h",  # INT16
        4: "I",  # UINT32
        5: "i",  # INT32
        6: "f",  # FLOAT32
        7: "?",  # BOOL
        10: "Q",  # UINT64
        11: "q",  # INT64
        12: "d",  # FLOAT64
    }
    TENSOR_TYPES = {
        0: "GGML_TYPE_F32",
        1: "GGML_TYPE_F16",
        2: "GGML_TYPE_Q4_0",
        3: "GGML_TYPE_Q4_1",
        6: "GGML_TYPE_Q5_0",
        7: "GGML_TYPE_Q5_1",
        8: "GGML_TYPE_Q8_0",
        9: "GGML_TYPE_Q8_1",
        10: "GGML_TYPE_Q2_K",
        11: "GGML_TYPE_Q3_K",
        12: "GGML_TYPE_Q4_K",
        13: "GGML_TYPE_Q5_K",
        14: "GGML_TYPE_Q6_K",
        15: "GGML_TYPE_Q8_K",
        16: "GGML_TYPE_IQ2_XXS",
        17: "GGML_TYPE_IQ2_XS",
        18: "GGML_TYPE_IQ3_XXS",
        19: "GGML_TYPE_IQ1_S",
        20: "GGML_TYPE_IQ4_NL",
        21: "GGML_TYPE_IQ3_S",
        22: "GGML_TYPE_IQ2_S",
        23: "GGML_TYPE_IQ4_XS",
        24: "GGML_TYPE_I8",
        25: "GGML_TYPE_I16",
        26: "GGML_TYPE_I32",
        27: "GGML_TYPE_I64",
        28: "GGML_TYPE_F64",
        29: "GGML_TYPE_IQ1_M",
    }

    def __init__(self, file_path: str, open_file: bool = True) -> None:
        super().__init__(file_path, open_file)
        self.magic_number = None
        self.version = None
        self.metadata = None
        self.tensors_info = None
        self.alignment = None

    def process(self) -> None:
        if not self.open_file:
            return
        try:
            with open(self.file_path, "rb") as f:
                # Read magic number
                self.magic_number = f.read(4)
                if self.magic_number != self.GGUF_MAGIC_NUMBER:
                    raise FileProcessingFailedError("Invalid GGUF magic number.")

                # Read version
                self.version = struct.unpack("I", f.read(4))[0]
                if self.version != 3:
                    raise FileProcessingFailedError("Unsupported GGUF version.")

                # Read tensor count and metadata key-value count
                tensor_count = struct.unpack("Q", f.read(8))[0]
                metadata_kv_count = struct.unpack("Q", f.read(8))[0]

                # Read metadata key-value pairs
                self.metadata = {}
                for _ in range(metadata_kv_count):
                    key, value = self._read_metadata_kv(f)
                    self.metadata[key] = value

                # Extract alignment
                self.alignment = self.metadata.get("general.alignment", 1)

                # Read tensor information
                self.tensors_info = []
                for _ in range(tensor_count):
                    tensor_info = self._read_tensor_info(f)
                    self.tensors_info.append(tensor_info)

                # Store extracted metadata
                self.metadata.update({
                    "magic_number": self.magic_number.decode("utf-8"),
                    "version": self.version,
                    "tensor_count": tensor_count,
                    "alignment": self.alignment,
                    "tensors_info": self.tensors_info
                })

        except Exception as e:
            raise FileProcessingFailedError(f"Error processing GGUF file {self.file_path}: {e}")

    def _read_string(self, f) -> str:
        """Reads a string from the file."""
        length = struct.unpack("Q", f.read(8))[0]
        return f.read(length).decode("utf-8")

    def _read_metadata_kv(self, f):
        """Reads a metadata key-value pair."""
        key = self._read_string(f)
        value_type = struct.unpack("I", f.read(4))[0]
        value = self._read_value(f, value_type)
        return key, value

    def _read_value(self, f, value_type):
        """Reads a value from the file based on its type."""
        if value_type in self.VALUE_FORMATS:
            return struct.unpack(
                self.VALUE_FORMATS[value_type],
                f.read(struct.calcsize(self.VALUE_FORMATS[value_type]))
            )[0]
        if value_type == 8:  # STRING
            return self._read_string(f)
        if value_type == 9:  # ARRAY
            array_type = struct.unpack("I", f.read(4))[0]
            array_len = struct.unpack("Q", f.read(8))[0]
            return [self._read_value(f, array_type) for _ in range(array_len)]
        raise FileProcessingFailedError(f"Unsupported GGUF value type: {value_type}")

    def _read_tensor_info(self, f) -> dict:
        """Reads tensor information from the file."""
        name = self._read_string(f)
        n_dimensions = struct.unpack("I", f.read(4))[0]
        dimensions = struct.unpack(f"{n_dimensions}Q", f.read(8 * n_dimensions))
        tensor_type = struct.unpack("I", f.read(4))[0]
        offset = struct.unpack("Q", f.read(8))[0]
        return {
            "name": name,
            "n_dimensions": n_dimensions,
            "dimensions": dimensions,
            "type": self.TENSOR_TYPES.get(tensor_type, "UNKNOWN"),
            "offset": offset
        }

    def save(self, output_path: str = None) -> None:
        """No save implementation needed for GGUF files (read-only)."""
        pass
