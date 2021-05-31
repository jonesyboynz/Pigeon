Write-Host "Cleaning workspace" -ForegroundColor green -BackgroundColor black

Write-Host "    Removing encoded files" -ForegroundColor cyan -BackgroundColor black
Get-ChildItem . -Include *.pgy -File -Recurse | foreach { Remove-Item -Path $_.FullName }

Write-Host "    Removing decoded files" -ForegroundColor cyan -BackgroundColor black
Get-ChildItem . -Include *.pgy-decoded -File -Recurse | foreach { Remove-Item -Path $_.FullName }

Write-Host "    Removing encoding files" -ForegroundColor cyan -BackgroundColor black
Get-ChildItem . -Include encodings/*.json -File -Recurse | foreach { Remove-Item -Path $_.FullName }
Get-ChildItem . -Include test/*.json -File -Recurse | foreach { Remove-Item -Path $_.FullName }

Write-Host "    Cleaning unit test files" -ForegroundColor cyan -BackgroundColor black
$FileName = "test/unit-tests/ut_pigeon.py"
if (Test-Path $FileName) {
  Remove-Item $FileName
}
