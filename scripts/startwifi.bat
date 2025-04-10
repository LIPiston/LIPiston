:: 作者: LIPiston
:: 与 wifi.ps1 一起使用

powershell.exe -command ^ "& {set-executionpolicy Remotesigned -Scope Process; .'.\wifi.ps1' }"