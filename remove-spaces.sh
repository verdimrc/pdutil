#!/usr/bin/env bash

declare INPUT=''
declare OUTPUT='output.csv'

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

echo "Remove all trailing whitespaces before/after comma on $INPUT" >&2

# <left_sed> | <mid_sed> | <right_sed>
# left_sed: remove '    ,'
# mid_sed: trim '"   ' and '   "'
# right_sed: remove '""'
sed -e 's/  *,/,/g' $INPUT | sed -e 's/  *"/"/g' -e 's/"  */"/g' | sed -e 's/""//g' > $OUTPUT
echo "Done"
