#! /bin/sh

./read < $1 | xargs -n1 sh -c 'echo $0 | base64	-d | rev | cut -c17- | h2b | hexdump -C'
