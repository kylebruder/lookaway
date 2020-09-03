#!/bin/bash
BUCKET="lookaway"
/bin/tar cp /home/lookaway/lookaway-env/lookaway/media | gzip | aws s3 cp - "s3://$BUCKET/backups/$(date '+20%y-%m-%d')/media.tar.gz"
/usr/bin/sudo -u postgres pg_dump lookaway > /tmp/lookaway.sql
/bin/gzip /tmp/lookaway.sql
/usr/local/bin/aws s3 cp /tmp/lookaway.sql.gz "s3://$BUCKET/backups/$(date '+20%y-%m-%d')/lookaway.sql.gz"
/bin/rm /tmp/lookaway.sql.gz
