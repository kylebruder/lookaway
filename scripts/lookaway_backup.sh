#!/bin/bash
###############################################################################
# Lookaway CMS backup script
# 
# A simple script to backup the database and media directory for Lookaway CMS.
# Run this script as the user that owns the data using sudo -u
# especially when calling it from a cron job.
# 
# CAUTION: Running this script more than once on a given calendar day
# will override previous backups made on that day.

# Set variables according to your specs.

keep_for=30 # Number of days worth of backups to keep
backup_dir="/home/lookaway/backups" # Your desired backup directory
lookaway_media_path="/home/lookaway/lookaway-env/lookaway/media" # The path to the lookaway media files
database="lookaway"

# Create today's backup dir.
today=$(date +%y-%m-%d)
if [ ! -d $backup_dir/$today ]; then
	echo "$(date) - Creating Lookaway backup dir $backup_dir/$today"
	/usr/bin/mkdir $backup_dir/$today
fi

# Dump the Database
/usr/bin/pg_dump lookaway > $backup_dir/$today/lookaway_db.sql 

# Create the archive
/usr/bin/tar cvfpz $backup_dir/$today/lookaway_media.tar.gz $lookaway_media_path

