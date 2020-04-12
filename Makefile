dist/glcube.app:
	pyinstaller --hidden-import pkg_resources.py2_warn -w glcube.py

dist/glcube:
	pyinstaller --hidden-import pkg_resources.py2_warn -F -w glcube.py

dist/glcube.exe:
	pyinstaller -w -F glcube.py

windows: clean dist/glcube.exe
macos: clean dist/glcube.app
linux: clean dist/glcube

clean:
	rm -rf ./__pycache__ ./build ./dist ./*.spec
