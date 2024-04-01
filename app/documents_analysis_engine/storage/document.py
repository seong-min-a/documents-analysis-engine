"""
Documents file Structure v0.0.2a 2024-04-01

[document]
    A record, which data structure composed of field and value pairs.    
    
[documents structure]
    ---------------------------------------------------------------
    file header
        EMPTY_STRING    : fixed  4 bytes
        MAGIC_STRING    : fixed  4 bytes
        EMPTY_STRING    : fixed 24 bytes
    ---------------------------------------------------------------
    documents block header
        BLOCK_SIZE      : fixed  8 bytes (compressed documents block size)
    ---------------------------------------------------------------        
    documents block data
        DOCUMENT_SIZE   : fixed  8 bytes (raw size, non-compressed)
        DOCUMENT        : variable, dict serialize 
    --------------------------------------------------------------- 
"""
import os
import gzip 
import pickle 
import constants 
import logging

logger = logging.getLogger(__name__)

class DocumentsWriter:
    def __init__(self):
        return 

    """
    Append only, document updates are not allowed
    """
    def write_documents(
        self,
        documents_file_path: str,
        documents: list, 
    ):
        with open(documents_file_path, 'a+b') as f:
            offset = f.tell() # == file byte size 
            if offset == 0:
                f.write(
                    b''.join(
                        [ # 32 bytes
                            b'\x00\x00\x00\x00', 
                            'DAE1'.encode('ascii'), # MAGIC
                            b'\x00\x00\x00\x00', 
                            b'\x00\x00\x00\x00',
                            b'\x00\x00\x00\x00', 
                            b'\x00\x00\x00\x00', 
                            b'\x00\x00\x00\x00', 
                            b'\x00\x00\x00\x00'
                        ]
                    )
                )
                offset = constants._DOCUMENTS_HEADER_BYTES
            else:
                pass

            # TODO. If received end of file or end of list signal, flush it
            documents_length = 0
            binary_documents = bytearray(b'')

            for document in documents:
                if isinstance(document, dict):
                    document_dict = document
                else:
                    document_dict = {constants._RAW_KEY: document}
                try:
                    serialized_document = pickle.dumps(document_dict)
                except Exception as e:
                    continue
                
                serialized_document_len = len(serialized_document)
                serialized_document_size = serialized_document_len.to_bytes(
                    constants._FIXED_DOCUMENT_SIZE_BYTES, 
                    byteorder=constants._BYTE_ORDER
                )
                binary_documents.extend(serialized_document_size)
                binary_documents.extend(serialized_document)
                documents_length += constants._FIXED_DOCUMENT_SIZE_BYTES + serialized_document_len
                if documents_length >= constants._BLOCK_SIZE:
                    documents_length = 0 
                    self.flush_block(f, binary_documents)
                    binary_documents = bytearray(b'')
            if documents_length > 0:
                self.flush_block(f, binary_documents)
            return

    def flush_block(
        self,
        file_io, 
        binary_documents,
    ):
        compressed_documents = gzip.compress(binary_documents)
        block_size_byte = len(compressed_documents).to_bytes(
            constants._FIXED_DOCUMENT_SIZE_BYTES, 
            byteorder=constants._BYTE_ORDER
        )
        file_io.write(
            b''.join([block_size_byte, compressed_documents])
        )
        return 

    def drop_documents(
        self,
        documents_file_path: str
    ):
        try:
            os.remove(documents_file_path)
        except Exception as e:
            logger.error(e) # ignore
            pass 
        return 

class DocumentsReader:
    def __init__(self):
        return 
    
    def read_documents(
        self,
        documents_file_path: str,
        limit: int = -1,
    ):
        try:
            with open(documents_file_path, 'rb') as f:
                block_offset = constants._DOCUMENTS_HEADER_BYTES
                documents_num = 1
                documents_file_size = os.stat(documents_file_path).st_size
                f.seek(block_offset)
                documents = []
                while block_offset < documents_file_size:
                    if limit != -1 and limit < documents_num:
                        break
                    block_size = int.from_bytes(
                        f.read(constants._FIXED_DOCUMENT_SIZE_BYTES), 
                        byteorder=constants._BYTE_ORDER
                    )
                    
                    block_offset += constants._FIXED_DOCUMENT_SIZE_BYTES  
                    f.seek(block_offset)
                    documents_block = f.read(block_size)
                    block_offset += block_size
                    decompressed_documents = self.decompress_block(
                        block_offset - constants._FIXED_DOCUMENT_SIZE_BYTES - block_size,
                        documents_block=documents_block
                    )
                    documents.extend(decompressed_documents)
                    documents_num += len(decompressed_documents)
                # TODO. yield
                if limit == -1:
                    return documents
                return documents[:limit]
        except FileNotFoundError as e:
            logger.error(e)
            raise FileNotFoundError(e)
        except Exception as e:
            logger.error(e)
            raise Exception(e)
            
    def read_documents_blocks(
        self,
        documents_file_path: str,
        limit: int = -1,
    ):
        try:
            with open(documents_file_path, 'rb') as f:
                block_offset = constants._DOCUMENTS_HEADER_BYTES
                documents_num = 1
                documents_file_size = os.stat(documents_file_path).st_size
                f.seek(block_offset)
                
                while block_offset < documents_file_size:
                    if limit != -1 and limit < documents_num:
                        break               
                    block_size = int.from_bytes(
                        f.read(constants._FIXED_DOCUMENT_SIZE_BYTES), 
                        byteorder=constants._BYTE_ORDER
                    )
                    
                    block_offset += constants._FIXED_DOCUMENT_SIZE_BYTES  
                    f.seek(block_offset)
                    documents_block = f.read(block_size)
                    block_offset += block_size
                    yield self.decompress_block(
                        block_offset - constants._FIXED_DOCUMENT_SIZE_BYTES - block_size,
                        documents_block=documents_block
                    )
        except FileNotFoundError as e:
            logger.error(e)
            raise FileNotFoundError(e)
        except Exception as e:
            logger.error(e)
            raise Exception(e)
    
    def decompress_block(
        self, 
        block_offset: int,
        documents_block: bytes, 
    ):
        decompressed_documents = gzip.decompress(documents_block)
        documents_byte_size = len(decompressed_documents)
        documents_offset = 0
        documents = []
        while documents_offset < documents_byte_size:
            document_dict = {          
                constants._DOCUMENT_OFFSET_KEY: documents_offset, 
                constants._BLOCK_OFFSET_KEY: block_offset,
            }
            document_size = int.from_bytes(
                decompressed_documents[
                    documents_offset:documents_offset+constants._FIXED_DOCUMENT_SIZE_BYTES
                ], 
                byteorder=constants._BYTE_ORDER
            )
            documents_offset += constants._FIXED_DOCUMENT_SIZE_BYTES
            binary_document = decompressed_documents[
                documents_offset:documents_offset+document_size
            ]
            documents_offset += document_size
            document_dict[constants._DOCUMENT_KEY] = pickle.loads(binary_document)
            documents.append(document_dict)
            # TODO. yield
        return documents