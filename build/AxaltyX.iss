; AxaltyX 安装脚本
; Inno Setup 6.0+

[Setup]
AppName=AxaltyX
AppVersion=1.0.0
AppPublisher=TBJ114
AppPublisherURL=
AppSupportURL=
AppUpdatesURL=
DefaultDirName={autopf}\AxaltyX
DefaultGroupName=AxaltyX
OutputDir=output
OutputBaseFilename=AxaltyX-Setup
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\AxaltyX.exe"; DestDir: "{app}"
Source: "..\axaltyx\resources\icons\app_icon.ico"; DestDir: "{app}\resources\icons"
Source: "..\axaltyx\i18n\*"; DestDir: "{app}\i18n"; Flags: recursesubdirs

[Icons]
Name: "{group}\AxaltyX"; Filename: "{app}\AxaltyX.exe"
Name: "{group}\Uninstall AxaltyX"; Filename: "{uninstallexe}"
Name: "{commondesktop}\AxaltyX"; Filename: "{app}\AxaltyX.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Run]
Filename: "{app}\AxaltyX.exe"; Description: "{cm:LaunchProgram,AxaltyX}"; Flags: nowait postinstall skipifsilent
