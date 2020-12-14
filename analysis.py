import sys
import os
import argparse
import csv
import itertools
import pathlib

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def debug_msg(dbg_color: str, dbg_type: str, *dbg_args: tuple) -> None:
    # since "technically" we could be getting a list in the mix with our string
    # we need to do some shenanigans of preparing the *args
    debug_message = []
    for arg in dbg_args:
        if isinstance(arg, str):
            debug_message.append([arg])
        elif isinstance(arg, list):
            debug_message.append(arg)
        
    debug_message = sum(debug_message, [])
    if args.verbose:
        print('[{}{}{}] : {}'.format(dbg_color, dbg_type , bcolors.ENDC, ' '.join(debug_message)))
    return

def build_file_list_from_folder(path: str) -> list:
    file_list = []
    for root, _, files in os.walk(path):
        for file in files:
            # ignore non .csv files
            if pathlib.Path(file).suffix == '.csv':
                file_list.append(os.path.join(root, file))
    return file_list

def read_file_contents(path: str) -> list:
    file_contents = []
    marketplace, group, _ = path.split('/')
    with open(path, 'r') as f:
        row_count = 0
        reader = csv.reader(f)
        for row in reader:
            # so we can use this data for later?
            row.insert(0, group)
            row.insert(0, marketplace)
            file_contents.append(row)
            row_count += 1
        debug_msg(bcolors.OKGREEN, 'STATUS', 'Processing file:', path, '({} entries)'.format(row_count))
    return file_contents

def remove_dupes(entries: list) -> list:
    stringed_entries = []
    for entry in entries:
        stringed_entries.append(','.join(entry))
    
    cleaned_entries = []
    temp_entries = []

    for i, entry in enumerate(stringed_entries):
        if entry not in temp_entries:
            temp_entries.append(entry)
            cleaned_entries.append(entries[i])

    return cleaned_entries

def main() -> None:
    if not args.folders:
        print('[{}ERROR{}] : No folders provided!'.format(
            bcolors.WARNING, bcolors.ENDC))
        sys.exit(-1)
    
    debug_msg(bcolors.OKGREEN, 'STATUS', 'Using verbose mode!')
    debug_msg(bcolors.OKGREEN, 'STATUS', 'Building file list...')
    # build individual file list (sum flattens the list!)
    file_list = sum([build_file_list_from_folder(folder) for folder in args.folders], [])
    debug_msg(bcolors.OKGREEN, 'STATUS', 'Built file list!')
    debug_msg(bcolors.OKGREEN, 'STATUS', 'Using list:', file_list)
    all_contents = []
    for file in file_list:
        # debug_msg(bcolors.OKGREEN, 'STATUS', 'Processing file:', file)
        all_contents.append(read_file_contents(file))

    # again, flatten the list
    all_contents = sum(all_contents, [])

    # remove duplicates
    debug_msg(bcolors.OKGREEN, 'STATUS', 'Removing duplicate entries...')
    cleaned_contents = remove_dupes(all_contents)
    debug_msg(bcolors.OKGREEN, 'STATUS', 'Removed {} duplicates'.format(len(all_contents) - len(cleaned_contents)))

    with open(args.file, 'w') as f:
        writer = csv.writer(f)
        for row in cleaned_contents:
            # schema for entry
            '''
            marketplace, 
            general-catagory, 
            vendor name, 
            market-specific catagory, 
            description, 
            price, 
            marketplace rating (optional)
            '''
            writer.writerow(row)

    debug_msg(bcolors.OKGREEN, 'STATUS', 'Written to file: {}'.format(args.file))
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Enables verbose logging.')
    parser.add_argument('-f', '--file', action='store', help='File to store all the data (overwrites an existing file)', required=True)
    parser.add_argument('folders', nargs='*', help='Folders to process')
    args = parser.parse_args()
    main()
