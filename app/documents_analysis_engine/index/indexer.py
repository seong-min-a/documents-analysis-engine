import pickle
from collections import defaultdict

class Indexer:
    def __init__(self):
        return 
    
    """
    output:
    ex> tokens_map = {
            token: inverted_index_line_number, 
            token: inverted_index_line_number, 
            ..., 
            token: inverted_index_line_number, 
        }
    """
    def write_once_index(
        self,
        index_file_path: str,
        tokens_dict: dict = None,
    ):
        tokens_map = defaultdict(int)
        with open(index_file_path, 'w') as f:
            token_line_num = 0
            for token, offset_list in tokens_dict.items():
                inverted_index = f'{token}:{",".join([str(offset) for offset in set(offset_list)])}\n'
                f.write(inverted_index)
                token_line_num += 1
                tokens_map[token] = token_line_num
        """
        TODO. increment index 
        """
        return tokens_map

    def write_tokens_map(
        self,
        tokens_map: dict,
        tokens_map_file_path: str
    ): 
        try:
            with open(tokens_map_file_path, 'wb') as f:
                pickle.dump(tokens_map, f)
                return 
        except Exception as e:
            print(e)
            return

    def load_tokens_map(
        self,
        tokens_map_file_path: str
    ):
        try:
            with open(tokens_map_file_path, 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError as e:
            print(e)
            raise e
        except Exception as e:
            print(e)
            raise e    