#!/bin/bash

directory=$1
command=$2
args=${*:3}

if [[ -z "$directory" ]]
then
    echo "empty directory"
    exit
fi

pushd ${directory} > /dev/null
case "$command" in
    -c | --compile)
        django-admin compilemessages
        ;;
    *)
        mkdir -p locale
        args="$2 $args"
        args="$(echo -e "${args}" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')"

        if [[ -z "$args" ]]
        then
            args="-l ru"
        fi

        django-admin makemessages --no-obsolete ${args}
        ;;
esac
popd > /dev/null
