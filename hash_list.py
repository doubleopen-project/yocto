#!/usr/bin/env python3
# Copyright (c) 2020 HH Partners, Attorneys-at-law Ltd
# SPDX-License-Identifier: MIT
# Author: Mikko Murto

import os
import json
import hashlib
import argparse
import glob
from tqdm import tqdm
from helpers import calculate_sha256
from classes import ElfFile, SourceFile, SourceListFile


# Loop over all srclist files and extract the data.

if __name__ == "__main__":
    # Initialize dictionary.
    result = {}
    # Build pkgdata folder.
    pkgdata_folder = "build/tmp/pkgdata/qemux86-64/"

    srclist_files = [
        file for file in os.listdir(pkgdata_folder) if file.endswith(".srclist")
    ]

    for file in tqdm(srclist_files):
        sourcelist_file_object = SourceListFile(pkgdata_folder + file)
        result[file] = {
            elf_file.file_name: elf_file.source_files_with_hashes
            for elf_file in sourcelist_file_object.elf_files
        }

    # Write the data to a file.
    with open("hash_list.json", "w") as f:
        json.dump(result, f, indent=4, sort_keys=True)
