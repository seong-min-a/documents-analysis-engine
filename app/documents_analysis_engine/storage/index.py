"""
Inverted index file Structure v0.0.2a 2024-04-01

[inverted index]
    An inverted index is a data structure used to store and organize 
    information for efficient search and retrieval. 

[index file structure]
    ---------------------------------------------------------------
    index file header   # fixed 32 bytes
        EMPTY_STRING    : fixed  4 bytes
        MAGIC_STRING    : fixed  4 bytes
        EMPTY_STRING    : fixed 24 bytes
    ---------------------------------------------------------------
    index block header
        BLOCK_SIZE      : fixed  8 bytes (compressed index block size)
    ---------------------------------------------------------------        
    index block data    # node in a linked list
        INDEX_DATA      : variable, dict serialize
    --------------------------------------------------------------- 

[index data]
    INDEX_DATA = serialize(
        b'token': {
                                       # int or long or long long
            'prev_index_block_offset': prev_index_block_offset, 
            block_offset: [         # int or long or long long 
                document_offset,    # int or long or long long 
                ...
                document_offset     # int or long or long long 
            ], ...
        }, ...
    )

[token map]
    token map = serialize(
        b'token': last_index_block_offset,
        b'token': last_index_block_offset,
        ...,
        b'token': last_index_block_offset,
    )
"""
import copy
import constants
import gzip
import pickle
import logging
from collections import defaultdict

logger = logging.getLogger(__name__)

class IndexBuilder:
    def __init__(
        self, 
        tokenize_func,
        index_column_name: str, 
        index_file_path: str, 
        index_block_offset_file_path: str,
    ):
        self.tokenize_func = tokenize_func
        self.index_column_name = index_column_name
        self.index_file_path = index_file_path
        self.index_block_offset_file_path = index_block_offset_file_path
        return 

    def flush_index_block(
        self,
        compressed_index_block: dict,
        compressed_index_block_size: int,
        index_file_path: str
    ):
        with open(index_file_path, 'a+b') as f:
            compressed_index_block_size_byte = compressed_index_block_size.to_bytes(
                constants._FIXED_INDEX_BLOCK_SIZE_BYTES, 
                byteorder=constants._BYTE_ORDER
            )
            byte_data = b''.join(
                [
                    compressed_index_block_size_byte,
                    compressed_index_block
                ]
            )
            f.write(
                byte_data
            )
        return 

    def write_index_map(
        self,
        index_block_offset_dict: dict, 
        index_block_offset_dict_file_path: str
    ):
        with open(index_block_offset_dict_file_path, 'wb') as f:
            f.write(pickle.dumps(index_block_offset_dict))
        return 

    def read_index_map(
        self, 
        index_block_offset_dict_file_path: str
    ):
        with open(index_block_offset_dict_file_path, 'rb') as f:
            return pickle.loads(f.read())
    
    def generate_nested_dict_offset_list(self):
        return defaultdict(list)
    def generate_nested_dict_token_key(self):
        return defaultdict(self.generate_nested_dict_offset_list)
    def get_index_data_dict(self):
        return defaultdict(self.generate_nested_dict_token_key)

    def build_index(
        self,
        documents_blocks, 
        index_block_offset_dict: dict
    ):
        index_data_dict = self.get_index_data_dict()
        
        prev_index_block_offset_dict = copy.deepcopy(index_block_offset_dict)
        curr_index_block_offset_dict = copy.deepcopy(index_block_offset_dict)
        
        compressed_index_block = None
        compressed_index_block_size = 0
        with open(self.index_file_path, 'a+b') as f:
            compressed_index_block_size_offset = f.tell()
            if compressed_index_block_size_offset == 0:
                f.write(
                    b''.join(
                        [ # 32 bytes
                            b'\x00\x00\x00\x00', 
                            'IDX1'.encode('ascii'), # MAGIC
                            b'\x00\x00\x00\x00', 
                            b'\x00\x00\x00\x00',
                            b'\x00\x00\x00\x00', 
                            b'\x00\x00\x00\x00', 
                            b'\x00\x00\x00\x00', 
                            b'\x00\x00\x00\x00'
                        ]
                    )
                )
                compressed_index_block_size_offset = constants._INDEX_HEADER_BYTES
        
        for documents in documents_blocks:
            if compressed_index_block_size > constants._FIXED_INDEX_BLOCK_SIZE_BYTES:
                self.flush_index_block(
                    compressed_index_block,
                    compressed_index_block_size,
                    self.index_file_path
                )
                index_data_dict = self.get_index_data_dict()
                compressed_index_block_size_offset += compressed_index_block_size + constants._FIXED_INDEX_BLOCK_SIZE_BYTES
                compressed_index_block = None
                compressed_index_block_size = 0
                prev_index_block_offset_dict = copy.deepcopy(curr_index_block_offset_dict)

            for document in documents:
                block_offset = document.get('block_offset')
                document_offset = document.get('document_offset')

                tokenized_set = self.tokenize_func(
                    document.get('document'),
                    self.index_column_name
                )
                for token in tokenized_set:

                    binary_token = token.encode('ascii')
                    index_data_dict[binary_token]['documents_offset'][block_offset].append(document_offset)
                    prev_index_block_offset = prev_index_block_offset_dict.get(binary_token, 0)
                    index_data_dict[binary_token]['prev_index_block_offset'] = prev_index_block_offset
                    curr_index_block_offset_dict[binary_token] = compressed_index_block_size_offset

            compressed_index_block = gzip.compress(pickle.dumps(dict(index_data_dict)))
            compressed_index_block_size = len(compressed_index_block)

        if compressed_index_block_size > 0:
            self.flush_index_block(
                compressed_index_block, 
                compressed_index_block_size,
                self.index_file_path
            )

        self.write_index_map(
            curr_index_block_offset_dict, 
            self.index_block_offset_file_path, 
        )
        return curr_index_block_offset_dict