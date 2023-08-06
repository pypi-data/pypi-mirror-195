#!/bin/bash

# build
python3 -m build

# update patch version
python3 update_version_on_file.py

# publish new version
USERNAME="vincent2303"
PASSWORD="g9sA3h7tY8#xFfYs"

echo "Uploading to PyPI..."
echo "$USERNAME" | python3 -m twine upload --skip-existing --username "$USERNAME" --password "$PASSWORD" dist/*