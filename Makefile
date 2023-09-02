build:
	py.exe -m build
	twine.exe upload dist/*