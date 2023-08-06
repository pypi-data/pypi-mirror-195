all: net-contextdiff

remake: clean all

net-contextdiff:
	./setup.py sdist bdist_wheel

upload:
	python3 -m twine upload dist/*

clean:
	rm -rf build dist net_contextdiff.egg-info
