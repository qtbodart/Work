
#! bin/bash

current_date="$(date +"%Y-%m-%d %H:%M:%S")"
backup_file=backup.tar
dir_to_compress=Test
log_file=compression.log

tar cf $backup_file $dir_to_compress

echo $current_date > $log_file

ls -R -l $dir_to_compress | awk '{print $9, $5}'
