:: author: LIPiston
:: Use with wifi.ps1

powershell.exe -command ^ "& {set-executionpolicy Remotesigned -Scope Process; .'.\wifi.ps1' }"