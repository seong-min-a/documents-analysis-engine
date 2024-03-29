import os, json
import gzip 
import constants 

class DocumentsReader:
    def __init__(self):
        return 
    
    def read_documents(
        self,
        documents_file_path: str,
        limit: int = 0,
    ):
        try:
            with open(documents_file_path, 'rb') as f:
                offset = 0
                documents_num = 1
                documents_file_size = os.stat(documents_file_path).st_size
                documents = []
                while offset < documents_file_size:
                    if limit != 0 and limit < documents_num:
                        break
                    document_size = int.from_bytes(
                        f.read(constants._FIXED_DOCUMENT_LENGTH_BYTE_SIZE), 
                        byteorder=constants._BYTE_ORDER
                    )
                    offset += constants._FIXED_DOCUMENT_LENGTH_BYTE_SIZE
                    f.seek(offset)
                    binary_document = f.read(document_size)
                    offset += document_size
                    document = gzip.decompress(binary_document)
                    documents.append(
                        {
                            constants._OFFSET: offset - document_size - constants._FIXED_DOCUMENT_LENGTH_BYTE_SIZE,
                            constants._DOCUMENT: json.loads(document)
                        }
                    )
                    documents_num += 1
                # TODO. yield
                return documents
        except FileNotFoundError as e:
            print(e)
            raise FileNotFoundError(e)
        except Exception as e:
            print(e)
            raise Exception(e)