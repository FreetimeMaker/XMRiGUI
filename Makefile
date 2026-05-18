APP_NAME = XMRiGUI
VERSION = 1.4.0
SCRIPT = xmrigui.py
ICON = xmrigui.png

.PHONY: all run build-linux build-windows clean deps

all: run

run:
	python3 $(SCRIPT)

build-linux:
	pyinstaller --onefile --windowed --name $(APP_NAME)-v$(VERSION) --icon=$(ICON) $(SCRIPT)

build-windows:
	# Note: This target is intended to be run in a Windows environment
	# or a shell with access to a Windows-based PyInstaller.
	pyinstaller --onefile --windowed --name $(APP_NAME)-v$(VERSION) --icon=$(ICON) $(SCRIPT)

clean:
	rm -rf build/ dist/ *.spec

deps:
	pip install PyQt6 pyinstaller