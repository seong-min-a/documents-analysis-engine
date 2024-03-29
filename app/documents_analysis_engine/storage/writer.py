import os
import constants 
import json
import gzip 

class DocumentsWriter:
    def __init__(self):
        return 
    
    def write_documents(
        self,
        documents_file_path: str,
        documents: list, 
    ):
        """
        append only
        """
        with open(documents_file_path, 'a+b') as f:
            offset_list = []
            offset = f.tell()
            for document in documents:
                if isinstance(document, dict):
                    document_dict = document
                else:
                    document_dict = {constants._SENTENCE: document}
                compressed_document = gzip.compress(
                    json.dumps(document_dict).encode(encoding=constants._STRING_ENCODER)
                )
                document_size = len(compressed_document).to_bytes(
                    constants._FIXED_DOCUMENT_LENGTH_BYTE_SIZE, 
                    byteorder=constants._BYTE_ORDER
                )
                binary_document = b''.join([
                    document_size, 
                    compressed_document
                ])
                write_byte_size = f.write(binary_document)
                offset += write_byte_size
                offset_list.append(offset)
            return offset_list

    def drop_documents(
        self,
        documents_file_path: str
    ):
        try:
            os.remove(documents_file_path)
        except Exception as e:
            print(e) # ignore
        return 
        