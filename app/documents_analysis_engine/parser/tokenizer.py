import re
from collections import defaultdict

class Tokenizer:
    def __init__(self):
        return 
    
    def tokenize(
        self,
        documents: list, 
        split_str: str = r'[\t\n`\-=~!@#$%^&*()_+\[\]{};\'\\:"|<,./<>? ]', 
        index_column_name: str = 'sentence',
        token_option: str = 'lower',
        # TODO. inject tokenizer
    ):
        tokens_dict = defaultdict(list)
        for document in documents:
            offset = document.get('offset')
            sentence = document.get('document', {}).get(index_column_name)
            if not isinstance(sentence, str):
                continue
            for token in re.split(split_str, sentence):
                if len(token) == 0:
                    continue
                if token_option == 'lower':
                    token = token.lower()
                elif token_option == 'upper': 
                    token = token.upper()
                else:
                    pass
                tokens_dict[token].append(offset)
        return tokens_dict