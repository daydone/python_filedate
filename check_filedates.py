import os
from datetime import datetime, timedelta

# Function to get file timestamps from file stat metadata
def get_file_timestamps(filepath):
    try:
        stat = os.stat(filepath)
        access_time = datetime.fromtimestamp(stat.st_atime)
        modify_time = datetime.fromtimestamp(stat.st_mtime)
        change_time = datetime.fromtimestamp(stat.st_ctime)
        return access_time, modify_time, change_time
    except Exception as e:
        return None, None, None, "Error retrieving date: {}".format(e)

# set media catalog filepath
catalog_file = '/text_file_of_files_paths'

#get the file paths from the catalog file
#need to add a filter to be able to specify partitions i.e. /media vs /media4
with open(catalog_file, 'r') as file:
    filepaths = file.readlines()

#format the file paths
filepaths = [filepath.strip() for filepath in filepaths]

# count total number of files
total_files = len(filepaths)

# set date to X days ago (90) currently
ninety_days_ago = datetime.now() - timedelta(days=180)

# Get timestamps with a counter
valid_files = []
for index, filepath in enumerate(filepaths, start=1):
    access_time, modify_time, change_time = get_file_timestamps(filepath)
    if access_time is None or modify_time is None or change_time is None:
        print("Skipping file due to error: {}".format(filepath))
        continue

    print("Processing {}/{}: {}   Modify: {}".format(
        index, total_files, filepath, modify_time.strftime('%Y-%m-%d %H:%M:%S')
    ))

    if (access_time < ninety_days_ago and
        modify_time < ninety_days_ago and
        change_time < ninety_days_ago):
        valid_files.append(filepath)

# Print the results change to delete operation when needed
for filepath in valid_files:
    print("Valid file: {}".format(filepath))

