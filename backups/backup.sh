#!/bin/bash
BUCKET="lookaway"
tar cp /home/lookaway/lookaway-env/lookaway/media | gzip | aws s3 cp - "s3://$BUCKET/backups/$(date '+20%y-%m-%d')/media.tar.gz"
sudo -u postgres pg_dump lookaway > /tmp/lookaway.sql
gzip /tmp/lookaway.sql
aws s3 cp /tmp/lookaway.sql.gz "s3://$BUCKET/backups/$(date '+20%y-%m-%d')/lookaway.sql.gz"
rm /tmp/lookaway.sql.gz
