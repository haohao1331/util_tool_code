import os
from pathlib import Path
import json

root_path = Path('/Volumes/09158606011/Multimedia')
# root_path = Path('/Users/haohao1331/Desktop/drive organization/Amazon Internship')


def traverse_dir(path : Path):
    current_dict = {
        'files': []
    }
    print(f'working on: {path}')
    for thing in path.iterdir():
        if thing.is_file():
            current_dict['files'].append(thing.name)
        elif thing.is_dir():
            current_dict[thing.name] = traverse_dir(thing)
        else:
            print(f'ERROR: {thing}')
    return current_dict
    
output = traverse_dir(root_path)


with open('names.json', 'w+') as f:
    f.write(json.dumps(output, indent=4))