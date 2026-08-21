.PHONY: install uninstall deb rpm

package = xmrigui_1.8.0_amd64

install:
	mkdir -p /opt/xmrigui
	mkdir -p /usr/share/icons/hicolor/256x256/apps
	cp xmrigui.png /usr/share/icons/hicolor/256x256/apps/
	cp /linux/xmrigui.desktop /usr/share/applications/

uninstall:
	rm /usr/local/bin/xmrigui
	rm -rf /opt/xmrigui
	rm /usr/share/icons/hicolor/256x256/apps/xmrigui.png
	rm /usr/share/applications/xmrigui.desktop

deb:
	mkdir -p $(package)/usr/local/bin/
	mkdir -p $(package)/opt/xmrigui/
	mkdir -p $(package)/usr/share/icons/hicolor/256x256/apps/
	mkdir -p $(package)/usr/share/applications/
	cp xmrigui.py $(package)/usr/local/bin/xmrigui
	chmod +x $(package)/usr/local/bin/xmrigui
	cp xmrig $(package)/opt/xmrigui/
	chmod +x $(package)/opt/xmrigui/xmrig
	cp xmrigui.png $(package)/usr/share/icons/hicolor/256x256/apps/
	cp xmrigui.png $(package)/usr/local/bin/
	cp xmrigui.desktop $(package)/usr/share/applications/
	dpkg-deb --build --root-owner-group $(package)

rpm:
	mkdir -p rpmbuild/SOURCES
	cp xmrigui.py xmrig xmrigui.png xmrigui.desktop rpmbuild/SOURCES/
	rpmbuild -bb --define "_topdir $(shell pwd)/rpmbuild" linux/xmrigui.spec
	cp rpmbuild/RPMS/x86_64/*.rpm .
	rm -rf rpmbuild
