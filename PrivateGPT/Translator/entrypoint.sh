#!/bin/bash
# entrypoint.sh

# Start the server with waitress-serve
waitress-serve --call 'privateGPT_server:main'