#!bin/bash

if [ $# -eq 0 ]; then
    echo "Not enough arguments given"
    echo "Usage : backup.sh <DIRECTORY_NAME> <NEW_BACKUP_NAME>"
    exit 1
fi

if [ !-d "$#1" ]; then
    echo "Directory name does not exist !"
    exit 1
fi

current_date="$(date +"%Y-%m-%d %H:%M:%S")"
backup_file="$2".tar.gz
dir_to_compress="$1"
log_file=compression.log

tar cvf $backup_file $dir_to_compress

echo $current_date > $log_file

ls -Rl $dir_to_compress | awk '{print $5, $9}' | sed '/^[[:space:]]*$/d' | sort -n -r >> $log_file

