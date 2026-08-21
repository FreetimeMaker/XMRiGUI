; Inno Setup Script for XMRiGUI
; To build the installer:
; 1. Run 'python build_windows.py' to generate 'dist/XMRiGUI.exe'
; 2. Open this file in Inno Setup and click 'Compile'

[Setup]
AppId={{D3F7B29E-8A5E-4B9B-B8A1-D9F5E67C9242}}
AppName=XMRiGUI
AppVersion=1.8.0
AppPublisher=Freetime Maker
AppPublisherURL=https://github.com/FreetimeMaker/XMRiGUI
AppSupportURL=https://github.com/FreetimeMaker/XMRiGUI/issues
AppUpdatesURL=https://github.com/FreetimeMaker/XMRiGUI/releases
DefaultDirName={autopf}\XMRiGUI
DefaultGroupName=XMRiGUI
AllowNoIcons=yes
; The following line specifies the icon for the installer itself
SetupIconFile=.\windows\xmrigui.ico
; Since there is no certificate, we inform the user
OutputBaseFilename=XMRiGUI_Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "german"; MessagesFile: "compiler:Languages\German.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\XMRiGUI.exe"; DestDir: "{app}"; Flags: ignoreversion
; Include assets
Source: "xmrigui.png"; DestDir: "{app}"; Flags: ignoreversion
Source: "windows\xmrigui.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\XMRiGUI"; Filename: "{app}\XMRiGUI.exe"; IconFilename: "{app}\xmrigui.ico"
Name: "{group}\{cm:UninstallProgram,XMRiGUI}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\XMRiGUI"; Filename: "{app}\XMRiGUI.exe"; Tasks: desktopicon; IconFilename: "{app}\xmrigui.ico"

[Run]
Filename: "{app}\XMRiGUI.exe"; Description: "{cm:LaunchProgram,XMRiGUI}"; Flags: nowait postinstall skipifsilent

[Code]
procedure InitializeWizard;
begin
  MsgBox('Important Security Note: This software is NOT digitally signed.' + #13#10#13#10 +
         'Windows SmartScreen may show a warning during installation. ' +
         'This is expected for open-source mining software. ' +
         'Please click "More Info" and then "Run Anyway" if prompted.', mbInformation, MB_OK);
end;
