dist/glcube.app:
	pyinstaller --hidden-import pkg_resources.py2_warn -w glcube.py
	cd dist
	zip -r glcube.zip glcube.app
	cd ..

dist/glcube:
	pyinstaller --hidden-import pkg_resources.py2_warn -F -w glcube.py

dist/glcube.exe:
	pyinstaller -w -F glcube.py

windows: dist/glcube.exe
macos: dist/glcube.app
linux: dist/glcube

clean:
	rm -rf ./__pycache__ ./build ./dist ./*.spec
