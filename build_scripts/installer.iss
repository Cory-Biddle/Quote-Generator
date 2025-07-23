[Setup]
AppName=PDFQuoteGenerator
AppVersion=1.0
DefaultDirName={autopf}\PDFQuoteGenerator
DefaultGroupName=PDFQuoteGenerator
OutputBaseFilename=PDFQuoteInstaller
Compression=lzma
SolidCompression=yes
SetupIconFile=assets\app_icon.ico
UninstallDisplayIcon={app}\main.exe

[Files]
Source: "dist\main.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "creds.json"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\PDF Quote Generator"; Filename: "{app}\main.exe"
Name: "{commondesktop}\PDF Quote Generator"; Filename: "{app}\main.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop shortcut"; GroupDescription: "Additional icons:"
