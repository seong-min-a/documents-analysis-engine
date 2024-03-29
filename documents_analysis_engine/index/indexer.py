from collections import defaultdict

class Indexer:
    def __init__(self):
        return 
    
    def write_once_index(
        self,
        tokens_dict: dict,
        index_file_path: str
    ):
        tokens_map = defaultdict(int)
        with open(index_file_path, 'w') as f:
            token_line_num = 0
            for token, offset_list in tokens_dict.items():
                inverted_index = f'{token}:{",".join([str(offset) for offset in set(offset_list)])}\n'
                f.write(inverted_index)
                token_line_num += 1
                tokens_map[token] = token_line_num
        return tokens_map

    