#!/usr/bin/env bash

declare INPUT=''
declare OUTPUT='session_json_escaped.csv'

parse_args() {
    while [[ $# -gt 0 ]]; do
        key="$1"
        case $key in 
        -h|--help)
            echo "Usage: ${BASH_SOURCE[0]} [INPUT] [-o|--output OUTPUT]"
            exit 0
            ;;
        -o|--output)
            OUTPUT="$2"
            shift 2
            ;;
        -*)
            echo "Unknown option: $1"
            exit 1
            ;;
        *)
            INPUT="$1"
            shift
            ;;
        esac
    done
}

parse_args "$@"

if [[ ! -f $INPUT ]]; then
    echo "Input file not found: $INPUT" >&2
    exit -1
fi

echo "Escaping $INPUT to $OUTPUT..."

# <left_sed> | <right_sed>
# left_sed: escape all \n or \r even if they've been escaped.
# right_sed: remove extra \ from escaped^2 string
sed -e 's/\\\([rn]\)/\\\\\1/g' $INPUT | sed -e 's/\\\(\\\\[nr]\)/\1/g' > $OUTPUT
echo "Done"
