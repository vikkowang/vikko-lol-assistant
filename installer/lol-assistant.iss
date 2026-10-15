; LOL 语音助手安装脚本
#define MyAppName "LOL助手"
#define MyAppVersion "1.0"
#define MyAppExeName "lol-assistant.exe"

[Setup]
AppId={{8E7F6A5B-4C3D-4E2F-9B1A-0D5C4B3A2F1E}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher=vikko
DefaultDirName={localappdata}\Programs\LOL助手
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
PrivilegesRequired=lowest
OutputDir=.
OutputBaseFilename=LOL-Setup
Compression=lzma2
SolidCompression=no
WizardStyle=modern
CloseApplications=yes
UninstallDisplayIcon={app}\{#MyAppExeName}

[Languages]
Name: "chinesesimp"; MessagesFile: "ChineseSimplified.isl"

[Tasks]
Name: "desktopicon"; Description: "创建桌面快捷方式"; GroupDescription: "附加任务:"

[Files]
Source: "..\dist\lol-assistant\*"; DestDir: "{app}"; Flags: recursesubdirs ignoreversion

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "立即运行 {#MyAppName}"; Flags: nowait postinstall skipifsilent
