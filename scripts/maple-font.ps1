# 作者 LIPiston
# 作用 下载最新版本的 MapleMono 字体

# 定义变量
$FontUrl = "https://github.com/subframe7536/maple-font/releases/latest/download/MapleMono-NF-CN-unhinted.zip"
$DestDir = "./maple"
$ZipFile = "MapleMono-NF-CN-unhinted.zip"

# 创建目标目录（如果不存在）
if (-not (Test-Path -Path $DestDir)) {
    New-Item -ItemType Directory -Path $DestDir | Out-Null
}

# 下载字体 zip 文件
Write-Host "Downloading font from $FontUrl..."
try {
    Invoke-WebRequest -Uri $FontUrl -OutFile $ZipFile -ErrorAction Stop
} catch {
    Write-Host "Failed to download the font. Exiting."
    exit 1
}

# 解压字体到目标目录
Write-Host "Extracting font to $DestDir..."
try {
    Expand-Archive -Path $ZipFile -DestinationPath $DestDir -Force
} catch {
    Write-Host "Failed to extract the font. Exiting."
    exit 1
}

# 清理 zip 文件
Write-Host "Cleaning up..."
Remove-Item -Path $ZipFile -Force

Write-Host "Font downloaded and extracted successfully to $DestDir."