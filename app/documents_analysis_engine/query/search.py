import constants
import gzip
import json
from itertools import islice

class Search:
    def __init__(self):
        return 
    
    def search(
        self,
        token: str, 
        tokens_map: dict, 
        index_file_path: str, 
        documents_file_path: str
    ):
        index_line_num = tokens_map.get(token)
        if isinstance(index_line_num, int): 
            with open(index_file_path, 'r') as f:
                index_info = list(islice(f, index_line_num-1, index_line_num))[0]
                token, offset_list = index_info.split(':')
                index_dict = {
                    constants._TOKEN: token,
                    constants._OFFSET_LIST: [int(offset) for offset in offset_list[:-1].split(',')]
                }
            with open(documents_file_path, 'rb') as f:
                documents = []
                for offset in index_dict[constants._OFFSET_LIST]:
                    f.seek(offset)
                    document_size = int.from_bytes(
                        f.read(constants._FIXED_DOCUMENT_LENGTH_BYTE_SIZE), 
                        constants._BYTE_ORDER
                    )
                    f.seek(offset + constants._FIXED_DOCUMENT_LENGTH_BYTE_SIZE)
                    b_document = f.read(document_size)
                    document = gzip.decompress(b_document)
                    documents.append(json.loads(document))
                return documents
        else:
            return