import os
import json
from crawl import crawl_web 

def load_data_from_local(filename: str, directory: str) -> tuple:

    file_path = os.path.join(directory, filename)
    with open(file_path, 'r') as file:
        data = json.load(file)
    print(f"data loaded from {file_path}")
    return data, filename.rsplit('.', 1)[0].replace('_', ' ')

