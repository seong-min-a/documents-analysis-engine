"""
Documents Structure v0.0.1a 2024-03-29

[document]
    A record, which data structure composed of field and value pairs.

[documents structure]
    {document_size_byte}{compress(document)}
    {document_size_byte}{compress(document)}
    ...
    {document_size_byte}{compress(document)}

    document_size_byte:
        fixed signed 8bytes (long long) ~9,223,372,036,854,775,807
        document_size_byte to long type == document_size
            seek(8)
            read(document_size)
    document: 
        compressed json string
        len(compress(document)) == document_size_byte

[inverted index]
    An inverted index is a data structure used to store and organize 
    information for efficient search and retrieval. 

[inverted index structure]
    {token}:[{offset},{offset},...,{offset}]
    {token}:[{offset},{offset},...,{offset}]
    ...
    {token}:[{offset},{offset},...,{offset}]

    token:
        term or word
    offset:
        offset == cumsum(len(each document))
        seek(offset) 
"""