; Resolution Changer Safe Version Installer Script
!define APPNAME "Resolution Changer"
!define COMPANYNAME "xKineticK"
!define DESCRIPTION "Change screen resolution for gaming - Safe Version"
!define VERSIONMAJOR 1
!define VERSIONMINOR 0
!define VERSIONBUILD 1

!define HELPURL "https://github.com/xKineticK/ResolutionChanger"
!define UPDATEURL "https://github.com/xKineticK/ResolutionChanger"
!define ABOUTURL "https://github.com/xKineticK/ResolutionChanger"

!define INSTALLSIZE 36000

RequestExecutionLevel admin
InstallDir "$PROGRAMFILES\${APPNAME}"

Name "${APPNAME} - Safe Version"
Icon "resources\images\icon.ico"
outFile "ResolutionChanger-Safe-Setup.exe"

!include LogicLib.nsh
!include MUI2.nsh

; Interface Settings
!define MUI_ABORTWARNING
!define MUI_ICON "resources\images\icon.ico"
!define MUI_UNICON "resources\images\icon.ico"

; Welcome page with antivirus info
!define MUI_WELCOMEPAGE_TEXT "This installer will install ${APPNAME} on your computer.$\r$\n$\r$\nThis is the SAFE VERSION optimized to reduce false positive antivirus detections.$\r$\n$\r$\nIf your antivirus still blocks the application, please add it to your whitelist or check our antivirus guide.$\r$\n$\r$\nClick Next to continue."

; Pages
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "LICENSE.txt"
!insertmacro MUI_PAGE_COMPONENTS
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

; Uninstaller pages
!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

; Languages
!insertmacro MUI_LANGUAGE "English"

!macro VerifyUserIsAdmin
UserInfo::GetAccountType
pop $0
${If} $0 != "admin"
    messageBox mb_iconstop "Administrator rights required to install ${APPNAME}!"
    setErrorLevel 740
    quit
${EndIf}
!macroend

function .onInit
    setShellVarContext all
    !insertmacro VerifyUserIsAdmin
functionEnd

; Main application files
Section "Resolution Changer Safe (required)" SecMain
    SectionIn RO
    
    SetOutPath $INSTDIR
    
    ; Copy the safe executable
    File "dist\ResolutionChanger-Safe.exe"
    
    ; Copy icon for shortcuts
    SetOutPath $INSTDIR\resources\images
    File "resources\images\icon.ico"
    
    ; Copy configuration templates and guides
    SetOutPath $INSTDIR\config
    File "src\config\default_settings.json"
    File "config\resolutions.json"
    
    SetOutPath $INSTDIR\docs
    File "ANTIVIRUS_GUIDE.md"
    File "CODE_SIGNING_GUIDE.md"
    
    ; Create uninstaller
    SetOutPath $INSTDIR
    WriteUninstaller "$INSTDIR\uninstall.exe"
    
    ; Registry entries
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "DisplayName" "${APPNAME} (Safe Version)"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "UninstallString" "$INSTDIR\uninstall.exe"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "InstallLocation" "$INSTDIR"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "DisplayIcon" "$INSTDIR\resources\images\icon.ico"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "Publisher" "${COMPANYNAME}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "DisplayVersion" "${VERSIONMAJOR}.${VERSIONMINOR}.${VERSIONBUILD}"
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "EstimatedSize" ${INSTALLSIZE}
    
    ; Create AppData directory
    CreateDirectory "$APPDATA\ResolutionChanger"
    
    ; Copy default configs if they don't exist
    IfFileExists "$APPDATA\ResolutionChanger\settings.json" +2 0
        CopyFiles "$INSTDIR\config\default_settings.json" "$APPDATA\ResolutionChanger\settings.json"
    
    IfFileExists "$APPDATA\ResolutionChanger\resolutions.json" +2 0
        CopyFiles "$INSTDIR\config\resolutions.json" "$APPDATA\ResolutionChanger\resolutions.json"
SectionEnd

; Start Menu shortcuts
Section "Start Menu Shortcuts" SecStartMenu
    CreateDirectory "$SMPROGRAMS\${COMPANYNAME}"
    CreateShortCut "$SMPROGRAMS\${COMPANYNAME}\${APPNAME}.lnk" "$INSTDIR\ResolutionChanger-Safe.exe" "" "$INSTDIR\resources\images\icon.ico" 0 SW_SHOWNORMAL "" "${DESCRIPTION}"
    CreateShortCut "$SMPROGRAMS\${COMPANYNAME}\Antivirus Guide.lnk" "$INSTDIR\docs\ANTIVIRUS_GUIDE.md" "" "$INSTDIR\resources\images\icon.ico" 0 SW_SHOWNORMAL "" "Antivirus troubleshooting guide"
    CreateShortCut "$SMPROGRAMS\${COMPANYNAME}\Uninstall ${APPNAME}.lnk" "$INSTDIR\uninstall.exe" "" "$INSTDIR\uninstall.exe" 0 SW_SHOWNORMAL "" "Uninstall ${APPNAME}"
SectionEnd

; Desktop shortcut
Section "Desktop Shortcut" SecDesktop
    CreateShortCut "$DESKTOP\${APPNAME}.lnk" "$INSTDIR\ResolutionChanger-Safe.exe" "" "$INSTDIR\resources\images\icon.ico" 0 SW_SHOWNORMAL "" "${DESCRIPTION}"
SectionEnd

; Section descriptions
LangString DESC_SecMain ${LANG_ENGLISH} "Main application executable optimized for antivirus compatibility (required)"
LangString DESC_SecStartMenu ${LANG_ENGLISH} "Create shortcuts in Start Menu with antivirus guide"
LangString DESC_SecDesktop ${LANG_ENGLISH} "Create shortcut on Desktop"

!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
  !insertmacro MUI_DESCRIPTION_TEXT ${SecMain} $(DESC_SecMain)
  !insertmacro MUI_DESCRIPTION_TEXT ${SecStartMenu} $(DESC_SecStartMenu)
  !insertmacro MUI_DESCRIPTION_TEXT ${SecDesktop} $(DESC_SecDesktop)
!insertmacro MUI_FUNCTION_DESCRIPTION_END

; Uninstaller
Section "Uninstall"
    ; Remove application files
    Delete "$INSTDIR\ResolutionChanger-Safe.exe"
    Delete "$INSTDIR\uninstall.exe"
    RMDir /r "$INSTDIR\resources"
    RMDir /r "$INSTDIR\config"
    RMDir /r "$INSTDIR\docs"
    RMDir "$INSTDIR"
    
    ; Remove shortcuts
    Delete "$SMPROGRAMS\${COMPANYNAME}\${APPNAME}.lnk"
    Delete "$SMPROGRAMS\${COMPANYNAME}\Antivirus Guide.lnk"
    Delete "$SMPROGRAMS\${COMPANYNAME}\Uninstall ${APPNAME}.lnk"
    RMDir "$SMPROGRAMS\${COMPANYNAME}"
    Delete "$DESKTOP\${APPNAME}.lnk"
    
    ; Ask about config files
    MessageBox MB_YESNO|MB_ICONQUESTION "Keep configuration files?" IDYES KeepConfig
    RMDir /r "$APPDATA\ResolutionChanger"
    KeepConfig:
    
    ; Remove registry
    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}"
SectionEnd