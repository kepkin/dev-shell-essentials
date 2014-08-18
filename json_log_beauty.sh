#!/usr/bin/bash

function json_log_beauty() {
	while read -r line; do
		echo $line | python -m json.tool;
	done
}
