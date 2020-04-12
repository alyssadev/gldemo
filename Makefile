macos:
	pyinstaller --hidden-import pkg_resources.py2_warn -w glcube.py

linux:
	pyinstaller --hidden-import pkg_resources.py2_warn -F -w glcube.py

windows:
	pyinstaller -w -F glcube.py
