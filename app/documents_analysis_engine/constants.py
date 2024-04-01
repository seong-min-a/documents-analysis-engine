_BYTE_ORDER     = 'big' # BIG endian 
_STRING_ENCODER = 'utf-8'
_DOCUMENTS_FILE_EXTENSION = '.dox'
_INDEX_FILE_EXTENSION     = '.idx'
_TOKEN_MAP_FILE_EXTENSION = '.map'

"""
Bytes of maxium data size define
"""
_DOCUMENTS_HEADER_BYTES = 32
_INDEX_HEADER_BYTES     = 32 
# 1048576 == 2 ** 20 bytes == 1 Mb
_BLOCK_SIZE       = 1048576
_INDEX_BLOCK_SIZE = 1048576 
# 8 bytes == (unsigned long long) == 9,223,372,036,854,775,807
_FIXED_DOCUMENT_SIZE_BYTES              = 8
_FIXED_INDEX_BLOCK_SIZE_BYTES           = 8
_FIXED_SERIALIZED_INDEX_DATA_SIZE_BYTES = 8
_FIXED_PREV_INDEX_BLOCK_OFFSET_BYTES    = 8
_FIXED_PREV_INDEX_BLOCK_INNER_INDEX_DATA_OFFSET_BYTES = 8 

"""
Reserved keys
    convention:
        1. only 2 bytes 
"""
# # real 
# _BLOCK_OFFSET_KEY     = b'bo'
# _DOCUMENT             = b'_d'
# _DOCUMENT_OFFSET_KEY  = b'do'
# _OFFSET_KEY           = b'_o'
# _OFFSET_LIST_KEY      = b'ol'
# _PREV_INDEX_BLOCK_OFFSET = b'prev_index_block_offset'
# _RAW_KEY              = b'_r'
# _TOKEN_KEY            = b'_t'
# # dev
_BLOCK_OFFSET_KEY        = 'block_offset'
_DOCUMENT_KEY            = 'document'
_DOCUMENT_OFFSET_KEY     = 'document_offset'
_OFFSET_KEY              = 'offset'
_OFFSET_LIST_KEY         = 'offset_list'
_PREV_INDEX_BLOCK_OFFSET = 'prev_index_block_offset'
_RAW_KEY                 = 'raw'
_TOKEN_KEY               = 'token'
_LAST_INDEX_BLOCK_OFFSET = 'last_index_block_offset'
_LAST_INDEX_BLOCK_INNER_DATA_OFFSET = 'last_index_block_inner_data_offset'