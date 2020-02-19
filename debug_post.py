import json
import subprocess
import time
from datetime import datetime

def find_files(file_name):
    command = ['locate', '-b', '\\' + file_name.rpartition('/')[2]]

    output = subprocess.Popen(command, stdout=subprocess.PIPE).communicate()[0]
    output = output.decode()

    search_results = output.split('\n')

    return search_results

with open('debug.json', 'r') as f:
    debug_dict = json.load(f)

starting_time = datetime.now()
input_list = list(set(debug_dict['no_hash_found_not_built_in']))
output_dict = {}


counter = 1
for file in input_list:
    print(f'{datetime.now()}: Processing file {counter} of {len(input_list)}.')
    counter += 1
    if len(file.rpartition('/')[2]) > 2:
        output_dict[file] = find_files(file)

ending_time = datetime.now()


with open('debug_post_2.json', 'w') as outfile:
    json.dump(output_dict, outfile, indent=4, sort_keys=True)
    # json.dump(sorted(list(set(debug_dict['no_hash_found_not_built_in']))), outfile, indent=4, sort_keys=True)

print(f'Processed {len(input_list)} files in {ending_time - starting_time}.')