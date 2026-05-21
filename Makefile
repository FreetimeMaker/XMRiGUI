.PHONY: install uninstall clean deb

package = xmrigui_1.7.0_amd64

install:
	cp xmrigui.py /usr/local/bin/xmrigui
	chmod +x /usr/local/bin/xmrigui
	mkdir -p /opt/xmrigui
	cp xmrig /opt/xmrigui/
	chmod +x /opt/xmrigui/xmrig
	mkdir -p /usr/share/icons/hicolor/256x256/apps
	cp xmrigui.png /usr/share/icons/hicolor/256x256/apps/
	cp xmrigui.desktop /usr/share/applications/

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
	cp xmrigui.desktop $(package)/usr/share/applications/
	dpkg-deb --build --root-owner-group $(package)