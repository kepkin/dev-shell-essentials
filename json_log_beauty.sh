#!/usr/bin/bash

# Usage info
function __json_log_beauty_show_help() {
cat << EOF
Usage: ${0##*/} [-hi] [-s regex pattern]
Pretty prints json from input stream. Each line must be a correct json string.
	
	-h          display this help and exit
	-s          process only those lines that match pattern. Otherwise print as it is
	-i          match pattern case-insensetive

Example:
cat file | json_log_beauty -i -s "error\|except"

EOF
}

function json_log_beauty() {	
	# Initialize our own variables:
	output_file=""
	match_string=""
	ignore=0
	
	OPTIND=1 # Reset is necessary if getopts was used previously in the script.  It is a good idea to make this local in a function.
	while getopts "his:" opt; do
		case "$opt" in
			h)
				__json_log_beauty_show_help
				return 0
				;;
			i)  ignore=1
				;;
			s)  match_string=$OPTARG
				;;
			'?')
				__json_log_beauty_show_help >&2
				return 1
				;;
		esac
	done
	shift "$((OPTIND-1))" # Shift off the options and optional --.

	sed_params="q1"
	if [ $ignore -eq 1 ]; then
		sed_params="I$sed_params"
	fi
	
	while read -r line; do
		if [ -z "$match_string" ]; then
			echo $line | python -m json.tool;
			continue
		fi

		if (echo $line | sed -n -e "/$match_string/$sed_params"); then
			echo $line
		else
			echo $line | python -m json.tool;
		fi
	done
}
