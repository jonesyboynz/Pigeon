Write-Host "Cleaning workspace" -ForegroundColor green -BackgroundColor black

Write-Host "    Removing encoded files" -ForegroundColor cyan -BackgroundColor black
Get-ChildItem . -Include *.pgy -File -Recurse | foreach { Remove-Item -Path $_.FullName }
