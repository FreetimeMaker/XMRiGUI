APP_NAME = XMRiGUI
VERSION = 1.5.0
MAIN_SCRIPT = xmrigui.py
ICON = xmrigui.png
INSTALL_DIR = /opt/$(APP_NAME)

.PHONY: all deb build-windows install clean deps

all: deb build-windows

deb:
	@echo "Building Debian package..."
	rm -rf build/$(APP_NAME)
	mkdir -p build/$(APP_NAME)/usr/bin
	mkdir -p build/$(APP_NAME)$(INSTALL_DIR)
	mkdir -p build/$(APP_NAME)/DEBIAN
	# Include everything from the debian folder (metadata like DEBIAN/control and assets)
	cp -r DEBIAN/* build/$(APP_NAME)/DEBIAN/
	chmod 755 build/$(APP_NAME)/DEBIAN
	chmod 644 build/$(APP_NAME)/DEBIAN/control
	
	cp $(MAIN_SCRIPT) build/$(APP_NAME)$(INSTALL_DIR)/
	cp $(ICON) build/$(APP_NAME)$(INSTALL_DIR)/
	
	# Create wrapper script
	echo '#!/bin/bash' > build/$(APP_NAME)/usr/bin/$(APP_NAME)
	echo 'python3 $(INSTALL_DIR)/$(MAIN_SCRIPT) "$$@"' >> build/$(APP_NAME)/usr/bin/$(APP_NAME)
	chmod +x build/$(APP_NAME)/usr/bin/$(APP_NAME)
	
	dpkg-deb --build build/$(APP_NAME)
	mv build/$(APP_NAME).deb $(APP_NAME)_$(VERSION)_amd64.deb
	@echo "Debian package created: $(APP_NAME)_$(VERSION)_amd64.deb"

build-windows:
	@echo "Building Windows executable..."
	pyinstaller --onefile --windowed --icon=$(ICON) --name $(APP_NAME) $(MAIN_SCRIPT)

install:
	@echo "Installing to $(INSTALL_DIR)..."
	mkdir -p $(DESTDIR)$(INSTALL_DIR)
	install -m 644 $(MAIN_SCRIPT) $(DESTDIR)$(INSTALL_DIR)/$(MAIN_SCRIPT)
	install -m 644 $(ICON) $(DESTDIR)$(INSTALL_DIR)/$(ICON)
	mkdir -p $(DESTDIR)/usr/bin
	echo '#!/bin/bash\npython3 $(INSTALL_DIR)/$(MAIN_SCRIPT) "$$@"' > $(DESTDIR)/usr/bin/$(APP_NAME)
	chmod 755 $(DESTDIR)/usr/bin/$(APP_NAME)

clean:
	rm -rf build/ dist/ __pycache__/ *.spec *.deb

deps:
	pip install PyQt6 pyinstaller Pillow