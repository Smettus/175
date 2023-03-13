' Created by: Tim De Smet
' Last edit: 13/03/2023
'
'  1  7777777 555555
' 111     777 55
'  11    777  555555
'  11   777      5555
' 111  777    555555
' -------[ ENJOY ]-------
' Put this file in the working directory
'   Opens the System (system.py), Controller (controller.py) and MatLAB file
'   from current working directory

' <-- Change these next strings -->
Dim systemcmd: systemcmd = "python system.py pendulum"
Dim controllercmd: controllercmd = "python controller.py"
Dim matlabfile: matlabfile = "matlab_script.m"


' <!-- Change at own risk --!>
Private const WaitTime = 300 ' ms, may need to increase this value... todo: check if window is open https://stackoverflow.com/questions/41621591/vbscript-send-key
Set WshShell = WScript.CreateObject("WScript.Shell")
Set objShell = CreateObject("Shell.Application")

' Run System
Call objShell.ShellExecute("C:\Windows\System32\cmd.exe" , "", "", "open", 2)
WScript.Sleep(WaitTime)
WshShell.SendKeys "C:\Applic\Anaconda3\Scripts\activate.bat C:\Applic\Anaconda3"
WshShell.SendKeys "{ENTER}"
WshShell.SendKeys systemcmd
WshShell.SendKeys "{ENTER}"

WScript.Sleep(WaitTime)

' Run Controller
Call objShell.ShellExecute("C:\Windows\System32\cmd.exe" , "", "", "open", 2)
WScript.Sleep(WaitTime)
WshShell.SendKeys "C:\Applic\Anaconda3\Scripts\activate.bat C:\Applic\Anaconda3"
WshShell.SendKeys "{ENTER}"
WshShell.SendKeys controllercmd
WshShell.SendKeys "{ENTER}"

WScript.Sleep(WaitTime + 200)

' Run MatLAB
scriptdir = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)
Call objShell.ShellExecute(scriptdir&"\"&matlabfile, "", "", "open", 2)
WScript.Quit