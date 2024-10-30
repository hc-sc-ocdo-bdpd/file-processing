import pytest
import os
from file_processing import File
from file_processing.processors.gguf_processor import GgufFileProcessor
from file_processing_test_data import get_test_files_path

test_files_path = get_test_files_path()

# Test data: path and expected key-value pair values for each file
gguf_test_data = [
    (test_files_path / 'tinystories-gpt-0.1-3m.Q2_K.gguf', {
        'general.architecture': 'gpt2',
        'general.name': 'Tinystories-gpt-0.1-3m',
        'gpt2.block_count': 8,
        'gpt2.context_length': 2048,
        'gpt2.embedding_length': 64,
        'gpt2.feed_forward_length': 256,
        'gpt2.attention.head_count': 16,
        'gpt2.attention.layer_norm_epsilon': 9.999999747378752e-06,
        'general.file_type': 10,
        'tokenizer.ggml.model': 'gpt2',
        'tokenizer.ggml.pre': 'gpt-2',
        'tokenizer.ggml.tokens': 50257,
        'tokenizer.ggml.token_type': 50257,
        'tokenizer.ggml.merges': 50000,
        'tokenizer.ggml.bos_token_id': 50256,
        'tokenizer.ggml.eos_token_id': 50256,
        'tokenizer.ggml.add_bos_token': False,
        'general.quantization_version': 2,
        'magic_number': 'GGUF',
        'version': 3,
        'tensor_count': 101,
        'alignment': 1,
        'tensors_info': 101
    }),
    (test_files_path / 'mistral-1L-tiny.IQ3_M.gguf', {
        'general.architecture': 'llama',
        'general.type': 'model',
        'general.name': 'Mistral 1L Tiny',
        'general.finetune': '1L-tiny',
        'general.basename': 'mistral',
        'general.size_label': '35M',
        'general.tags': 1,
        'general.datasets': 1,
        'llama.block_count': 1,
        'llama.context_length': 2048,
        'llama.embedding_length': 512,
        'llama.feed_forward_length': 1024,
        'llama.attention.head_count': 16,
        'llama.attention.head_count_kv': 8,
        'llama.rope.freq_base': 10000.0,
        'llama.attention.layer_norm_rms_epsilon': 9.999999974752427e-07,
        'general.file_type': 27,
        'llama.vocab_size': 32000,
        'llama.rope.dimension_count': 32,
        'tokenizer.ggml.model': 'llama',
        'tokenizer.ggml.pre': 'default',
        'tokenizer.ggml.tokens': 32000,
        'tokenizer.ggml.scores': 32000,
        'tokenizer.ggml.token_type': 32000,
        'tokenizer.ggml.bos_token_id': 1,
        'tokenizer.ggml.eos_token_id': 2,
        'general.quantization_version': 2,
        'magic_number': 'GGUF',
        'version': 3,
        'tensor_count': 12,
        'alignment': 1,
        'tensors_info': 12
    })
]

@pytest.mark.parametrize("file_path, expected_metadata", gguf_test_data)
def test_gguf_metadata(file_path, expected_metadata):
    file_obj = File(file_path)

    # Check if the processor has the correct metadata attributes and values
    for key, expected_value in expected_metadata.items():
        assert key in file_obj.metadata, f"Missing key: {key}"
        actual_value = file_obj.metadata[key]
        
        if isinstance(expected_value, int):  # Check length for large lists
            if isinstance(actual_value, list):
                assert len(actual_value) == expected_value, f"Length mismatch for key: {key}"
            else:
                assert actual_value == expected_value, f"Value mismatch for key: {key}"
        else:  # Check actual value for smaller attributes
            assert str(actual_value) == str(expected_value), f"Value mismatch for key: {key}"
