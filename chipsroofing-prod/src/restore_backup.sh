#!/bin/bash
# Example: ./restore_backup.sh ../backup/18_09_2015.zip ../

archive=$1
directory=${2:-$(dirname ~+)}

unzip -o ${archive} media/* -d ${directory}/
unzip -o ${archive} dump.json
python3 manage.py loaddata --ignorenonexistent dump.json

if [[ -f dump.json ]];
then
  rm dump.json;
else
  echo "Warning! File dump.json not found!";
fi
