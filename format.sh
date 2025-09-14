#!/bin/bash
set -e

poetry run black .
poetry run isort .
echo "done."
