param (
    [Parameter(Mandatory=$true)]
    [string]$filePath
)

# 替换为你的 emacs.exe 文件的实际路径
$emacsPath = "D:\programes\emacs\bin\emacsclientw.exe"

# 在 PowerShell 中设置 HOME 环境变量为你的配置文件所在的目录(不能带\.emacs.d)
$env:HOME = "C:\Users\pc\AppData\Roaming"

Write-Host "emacsPath: $emacsPath"

# 启动新的进程
Start-Process -FilePath $emacsPath -ArgumentList $filePath

