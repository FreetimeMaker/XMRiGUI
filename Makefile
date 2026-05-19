APP_NAME = xmrigui
VERSION = 1.4.0
MAIN_SCRIPT = xmrigui.py
ICON = xmrigui.png
INSTALL_DIR = /opt/$(APP_NAME)

.PHONY: all deb build-windows install clean

all: deb build-windows

deb:
	@echo "Building Debian package..."
	mkdir -p build/$(APP_NAME)/DEBIAN
	mkdir -p build/$(APP_NAME)/usr/bin
	mkdir -p build/$(APP_NAME)$(INSTALL_DIR)
	
	cp $(MAIN_SCRIPT) build/$(APP_NAME)$(INSTALL_DIR)/
	cp $(ICON) build/$(APP_NAME)$(INSTALL_DIR)/
	
	# Create wrapper script for the binary path
	echo '#!/bin/bash' > build/$(APP_NAME)/usr/bin/$(APP_NAME)
	echo 'python3 $(INSTALL_DIR)/$(MAIN_SCRIPT) "$$@"' >> build/$(APP_NAME)/usr/bin/$(APP_NAME)
	chmod +x build/$(APP_NAME)/usr/bin/$(APP_NAME)
	
	# Generate control file
	echo "Package: $(APP_NAME)" > build/$(APP_NAME)/DEBIAN/control
	echo "Version: $(VERSION)" >> build/$(APP_NAME)/DEBIAN/control
	echo "Section: utils" >> build/$(APP_NAME)/DEBIAN/control
	echo "Priority: optional" >> build/$(APP_NAME)/DEBIAN/control
	echo "Architecture: all" >> build/$(APP_NAME)/DEBIAN/control
	echo "Depends: python3, python3-pyqt6" >> build/$(APP_NAME)/DEBIAN/control
	echo "Maintainer: Freetime Maker" >> build/$(APP_NAME)/DEBIAN/control
	echo "Description: A graphical user interface for XMRig crypto miner." >> build/$(APP_NAME)/DEBIAN/control
	
	dpkg-deb --build build/$(APP_NAME)
	mv build/$(APP_NAME).deb $(APP_NAME)_$(VERSION)_all.deb
	@echo "Debian package created: $(APP_NAME)_$(VERSION)_all.deb"

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