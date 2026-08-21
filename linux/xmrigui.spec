Name:           xmrigui
Version:        1.8.1
Release:        1%{?dist}
Summary:        GUI for XMRig crypto miner
License:        Apache-2.0
URL:            https://github.com/FreetimeMaker/XMRiGUI
BuildArch:      x86_64

Requires:       python3 >= 3.6, python3-pip, libuv, python3-gobject, gtk3

%description
XMRiGUI is a free and open-source crypto miner GUI for XMRig.

%install
mkdir -p %{buildroot}/usr/local/bin
mkdir -p %{buildroot}/opt/xmrigui
mkdir -p %{buildroot}/usr/share/icons/hicolor/256x256/apps
mkdir -p %{buildroot}/usr/share/applications

cp %{_sourcedir}/xmrigui.py %{buildroot}/usr/local/bin/xmrigui
chmod +x %{buildroot}/usr/local/bin/xmrigui
cp %{_sourcedir}/xmrig %{buildroot}/opt/xmrigui/xmrig
chmod +x %{buildroot}/opt/xmrigui/xmrig
cp %{_sourcedir}/xmrigui.png %{buildroot}/usr/share/icons/hicolor/256x256/apps/
cp %{_sourcedir}/xmrigui.desktop %{buildroot}/usr/share/applications/

%files
/usr/local/bin/xmrigui
/opt/xmrigui/xmrig
/usr/share/icons/hicolor/256x256/apps/xmrigui.png
/usr/share/applications/xmrigui.desktop

%changelog
* Fri Aug 21 2026 Freetime Maker <jamieachatz@gmail.com> - 1.8.1
