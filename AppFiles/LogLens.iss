[Setup]
AppName=LogLens
AppVersion=1.0
DefaultDirName={pf}\LogLens
DefaultGroupName=LogLens
OutputBaseFilename=LogLens
Compression=lzma
SolidCompression=yes
DisableWelcomePage=no
PrivilegesRequired=admin
SetupIconFile=C:\Users\focus\Desktop\AppFiles\loglens.ico

[Files]
; Installers (temporary directory)
Source: "C:\Users\focus\Desktop\AppFiles\python-installer.exe"; DestDir: "{tmp}"; Flags: deleteafterinstall
Source: "C:\Users\focus\Desktop\AppFiles\ollama-installer.exe"; DestDir: "{tmp}"; Flags: deleteafterinstall

; Main App Files
Source: "C:\Users\focus\Desktop\AppFiles\processing.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\focus\Desktop\AppFiles\fetching.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\focus\Desktop\AppFiles\analysis.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\focus\Desktop\AppFiles\launch_menu.ps1"; DestDir: "{app}"; Flags: ignoreversion

[Run]
; Install Python silently
Filename: "{tmp}\python-installer.exe"; Parameters: "/quiet InstallAllUsers=1 PrependPath=1"; StatusMsg: "Installing Python..."; Flags: skipifdoesntexist waituntilterminated

; Install Ollama silently
Filename: "{tmp}\ollama-installer.exe"; Parameters: "/silent"; StatusMsg: "Installing Ollama..."; Flags: skipifdoesntexist waituntilterminated

; Launch PowerShell menu after install (current user)
Filename: "powershell.exe"; Parameters: "-NoExit -ExecutionPolicy Bypass -File ""{app}\launch_menu.ps1"""; Flags: postinstall runascurrentuser

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop icon"; GroupDescription: "Additional icons:"

[Icons]
; Start menu icon
Name: "{group}\LogLens Launcher"; Filename: "powershell.exe"; Parameters: "-NoExit -ExecutionPolicy Bypass -File ""{app}\launch_menu.ps1"""

; Optional desktop icon
Name: "{userdesktop}\LogLens Launcher"; Filename: "powershell.exe"; Parameters: "-NoExit -ExecutionPolicy Bypass -File ""{app}\launch_menu.ps1"""; Tasks: desktopicon
