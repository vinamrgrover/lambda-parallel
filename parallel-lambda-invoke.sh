#!/bin/zsh

for num in {10..141..10}; do
	low=$((num - 10))
	high=$num
	echo Triggering for zip codes $low - $high
	sleep 3

	aws lambda invoke \
		--cli-binary-format raw-in-base64-out \
		--function-name batch-func \
		--payload "{ \"low\": $low, \"high\" : $high }" \
		response.json >>/dev/null &

done
wait
