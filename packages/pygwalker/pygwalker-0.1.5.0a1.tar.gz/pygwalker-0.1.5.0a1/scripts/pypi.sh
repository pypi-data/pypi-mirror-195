HERE=$(dirname $(dirname $0) )
python -m build && python -m twine upload $HERE/dist/* --skip-existing