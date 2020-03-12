from helpers import calculate_sha256
import json


class SourceFile:
    possible_locations = []

    def __init__(self, elf_file_folder, source_file):
        self.source_file = source_file
        self.elf_file_folder = elf_file_folder
        self.possible_locations = [
            elf_file_folder + "/package" + source_file,
            elf_file_folder + "/recipe-sysroot" + source_file,
            elf_file_folder + "/recipe-sysroot-native" + source_file,
            (elf_file_folder + "/" + "/".join(source_file.split("/")[4:])),
            "/".join(elf_file_folder.split("/")[:8])
            + "/"
            + "/".join(source_file.split("/")[4:]),
            "/".join(elf_file_folder.split("/")[:6])
            + "/"
            + "/".join(source_file.split("/")[2:]),
            # TODO Needs to be fixed.
            # "/".join(elf_file_folder.split("/")[:8]) + "/" + "/".join(source_file_name_list[4:]),
        ]

        source_file_name_list = source_file.split("/")

        if "build" in source_file_name_list:
            for i, v in enumerate(source_file_name_list):
                if v == "build":
                    source_file_name_list[i] = (
                        source_file.split("/")[i - 2]
                        + "-"
                        + source_file.split("/")[i - 1].split("-")[0]
                    )

        self.possible_locations.append(
            "/".join(elf_file_folder.split("/")[:8])
            + "/"
            + "/".join(source_file_name_list[4:])
        )

    def calculate_hash(self):
        result_dict = {}
        for i in self.possible_locations:
            sha_value = calculate_sha256(i)
            if sha_value:
                result_dict.setdefault(sha_value, []).append(i)
        if any(result_dict):
            return result_dict
        else:
            return {}


class ElfFile:
    def __init__(self, elf_file, source_files):
        self.file_name = elf_file
        self.folder = "/".join(elf_file.split("/", 10)[:10])
        self.source_files = [SourceFile(self.folder, i) for i in source_files]
        self.source_files_with_hashes = {
            i.source_file: i.calculate_hash() for i in self.source_files
        }


class SourceListFile:
    def __init__(self, srclist):
        with open(srclist) as f:
            data = json.load(f)
            self.elf_files = [ElfFile(k, v) for k, v in data.items()]
