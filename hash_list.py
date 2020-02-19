#!/usr/bin/env python3
# Copyright (c) 2020 HH Partners, Attorneys-at-law Ltd
# SPDX-License-Identifier: MIT
# Author: Mikko Murto

import os
import json
import hashlib
import argparse
import glob

# Buffer size for hash calculation.
BUF_SIZE = 65536

debug_dict = {
    'hash_list': [],
    'elf_list': [],
    'source_list': [],
    'no_hash_found': [],
    'no_hash_found_built_in': [],
    'no_hash_found_not_built_in': [],
    'duplicate_hash_found': [], 
}

# Build pkgdata folder.
pkgdata_folder = "build/tmp/pkgdata/qemux86-64/"

# Parse for '--debug' argument.
parser = argparse.ArgumentParser()
parser.add_argument('--debug', action='store_true')
debug = parser.parse_args().debug
if debug:
    print("DEBUG MODE ON!")

# Calculate SHA256 hash for a file.
# https://stackoverflow.com/questions/22058048/hashing-a-file-in-python
def calculate_sha256(file):
    try:
        sha256 = hashlib.sha256()

        with open(file, 'rb') as f:
            while True:
                data = f.read(BUF_SIZE)
                if not data:
                    break
                sha256.update(data)
        if debug:
            debug_dict['hash_list'].append(sha256.hexdigest())
        return sha256.hexdigest()
    except:
        return None

# Try to calculate hash for all possible source file locations.
def try_sha256(elf_file_folder, source_file):
    try:
        return calculate_sha256(elf_file_folder + '/package' + source_file)
    except:
        try:
            return calculate_sha256(elf_file_folder + '/recipe-sysroot' + source_file)
        except:
            try:
                return calculate_sha256(elf_file_folder + '/recipe-sysroot-native' + source_file)
            except:
                try:
                    path = "/".join(elf_file_folder.split("/", 8)[:8])
                    return calculate_sha256(path + "/" + "/".join(source_file.split("/", 4)[4:]))
                    # "/home/yocto/poky/build/tmp/work/core2-64-poky-linux/"
                except:
                    return None

# Debug function, return hash for each location, None if not found at the location.

location_counter = {
    'location_1': 0,
    'location_2': 0,
    'location_3': 0,
    'location_4': 0,
    'location_5': 0,
    'location_6': 0,
    'location_7': 0
}
def debug_sha256(elf_file_folder, source_file, location_counter):
    debug_dictionary = {}

    debug_dictionary['1: ' + elf_file_folder + '/package' + source_file] = calculate_sha256(elf_file_folder + '/package' + source_file)
    if debug_dictionary['1: ' + elf_file_folder + '/package' + source_file]:
        location_counter['location_1'] += 1

    debug_dictionary['2: ' + elf_file_folder + '/recipe-sysroot' + source_file] = calculate_sha256(elf_file_folder + '/recipe-sysroot' + source_file)
    if debug_dictionary['2: ' + elf_file_folder + '/recipe-sysroot' + source_file]:
        location_counter['location_2'] += 1


    debug_dictionary['3: ' + elf_file_folder + '/recipe-sysroot-native' + source_file] = calculate_sha256(elf_file_folder + '/recipe-sysroot-native' + source_file)
    if debug_dictionary['3: ' + elf_file_folder + '/recipe-sysroot-native' + source_file]:
        location_counter['location_3'] += 1

    debug_dictionary['4: ' + (elf_file_folder + "/" + "/".join(source_file.split("/")[4:]))] = calculate_sha256((elf_file_folder + "/" + "/".join(source_file.split("/")[4:])))
    if debug_dictionary['4: ' + (elf_file_folder + "/" + "/".join(source_file.split("/")[4:]))]:
        location_counter['location_4'] += 1

    debug_dictionary['5: ' + "/".join(elf_file_folder.split("/")[:8]) + "/" + "/".join(source_file.split("/")[4:])] = calculate_sha256("/".join(elf_file_folder.split("/")[:8]) + "/" + "/".join(source_file.split("/")[4:]))
    if debug_dictionary['5: ' + "/".join(elf_file_folder.split("/")[:8]) + "/" + "/".join(source_file.split("/")[4:])]:
        location_counter['location_5'] += 1

    debug_dictionary['6: ' + "/".join(elf_file_folder.split("/")[:6]) + "/" + "/".join(source_file.split("/")[2:])] = calculate_sha256("/".join(elf_file_folder.split("/")[:6]) + "/" + "/".join(source_file.split("/")[2:]))
    if debug_dictionary['6: ' + "/".join(elf_file_folder.split("/")[:6]) + "/" + "/".join(source_file.split("/")[2:])]:
        location_counter['location_6'] += 1

    source_file_name_list = source_file.split("/")
    if 'build' in source_file_name_list:       
        for i, v in enumerate(source_file_name_list):
            if v == 'build':
                source_file_name_list[i] = source_file.split("/")[i-2] + "-" + source_file.split("/")[i-1].split("-")[0]
                
        debug_dictionary['7: ' + "/".join(elf_file_folder.split("/")[:8]) + "/" + "/".join(source_file_name_list[4:])] = calculate_sha256("/".join(elf_file_folder.split("/")[:8]) + "/" + "/".join(source_file_name_list[4:]))
        if debug_dictionary['7: ' + "/".join(elf_file_folder.split("/")[:8]) + "/" + "/".join(source_file_name_list[4:])]:
            location_counter['location_7'] += 1
    else:
        debug_dictionary['7: not available'] = None

    return debug_dictionary


hash_dictionary = {}

srclist_amount = len(glob.glob1(pkgdata_folder, '*.srclist'))
srclist_current_counter = 1

# Loop over all srclist files and extract the data.
for file in os.listdir(pkgdata_folder):
    if file.endswith('.srclist'):

        # Progress 
        print(f"Currently processing srclist {srclist_current_counter} of {srclist_amount} total.", end='\r')
        srclist_current_counter += 1

        with open(pkgdata_folder + file) as srclist_file:
            hash_dictionary[file] = {}
            data = json.load(srclist_file)

            # Loop over all ELF files in srclist.
            for elf_file, source_files in data.items():
                hash_dictionary[file][elf_file] = {}
                elf_file_folder = "/".join(elf_file.split("/", 10)[:10])

                if debug:
                    debug_dict['elf_list'].append(elf_file)

                # Loop over all source files of the ELF file.
                for source_file in source_files:
                    hash_dictionary[file][elf_file][source_file] = try_sha256(elf_file_folder, source_file)
                   
                    if debug:
                        hash_dictionary[file][elf_file][source_file] = debug_sha256(elf_file_folder, source_file, location_counter)
                        debug_dict['source_list'].append(source_file)

                        if not any(value for value in hash_dictionary[file][elf_file][source_file].values()):
                            debug_dict['no_hash_found'].append(source_file)
                        
                        hashes = []
                    
                        for location, hash_value in hash_dictionary[file][elf_file][source_file].items():
                            if hash_value:
                                hashes.append(hash_value)
                        
                        if len(set(hashes)) > 1:
                            debug_dict['duplicate_hash_found'].append(hash_dictionary[file][elf_file][source_file])
                            



print()

# Write the data to a file.
print('Writing data to hash_list.json.')
with open('hash_list.json', 'w') as outfile:
    json.dump(hash_dictionary, outfile, indent=4, sort_keys=True)



if debug:
    print(f'Total elf files: {len(debug_dict["elf_list"])}.')
    print(f'Unique elf files: {len(set(debug_dict["elf_list"]))}')
    print(f'Total source files: {len(debug_dict["source_list"])}.')
    print(f'Unique source files: {len(set(debug_dict["source_list"]))}.')
    print(f'Total hash values: {len(debug_dict["hash_list"])}.')
    print(f'Unique hash values: {len(set(debug_dict["hash_list"]))}.')
    print(f'Sources, no hash: {len(debug_dict["no_hash_found"])}.')
    print(f'Sources, no hash, unique: {len(set(debug_dict["no_hash_found"]))}.')

    no_hash_found_built_in = []
    for source in debug_dict['no_hash_found']:
        if '<built-in>' in source:
            debug_dict['no_hash_found_built_in'].append(source)
        if '<built-in>' not in source:
            debug_dict['no_hash_found_not_built_in'].append(source)

    print(f'Sources, no hash, <built-in>: {len(debug_dict["no_hash_found_built_in"])}.')
    print(f'Sources, no hash, <built-in>, unique: {len(set(debug_dict["no_hash_found_built_in"]))}.')
    print(f'Sources, no hash, not <built-in>: {len(debug_dict["no_hash_found_not_built_in"])}.')
    print(f'Sources, no hash, not <built-in>, unique: {len(set(debug_dict["no_hash_found_not_built_in"]))}.')
    print(f'Sources, conflicting hash values: {len(debug_dict["duplicate_hash_found"])}')
    print()
    print(f'Location 1: {location_counter["location_1"]}.')
    print(f'Location 2: {location_counter["location_2"]}.')
    print(f'Location 3: {location_counter["location_3"]}.')
    print(f'Location 4: {location_counter["location_4"]}.')
    print(f'Location 5: {location_counter["location_5"]}.')
    print(f'Location 6: {location_counter["location_6"]}.')
    print(f'Location 7: {location_counter["location_7"]}.')
    new_list = []
    counts = []

    for dict_ in debug_dict["duplicate_hash_found"]:
        try:
            i = new_list.index(dict_)
        except ValueError:
            counts.append(1)
            new_list.append(dict_)
        else:
            counts[i] += 1

    assert len(counts) == len(new_list)
    for dict_, count in zip(new_list, counts):
        dict_['cnt'] = count

    del counts

    debug_dict["duplicate_hash_found_unique"] = new_list

    print(f'Sources, conflicting hash values, unique: {len(debug_dict["duplicate_hash_found_unique"])}.')

    print('Writing debug data to debug.json.')
    with open('debug.json', 'w') as outfile:
        json.dump(debug_dict, outfile, indent=4, sort_keys=True)
