Write-Host "Running Clean" -ForegroundColor yellow -BackgroundColor black

Write-Host "Cleaning workspace" -ForegroundColor green -BackgroundColor black

Write-Host "    Removing encoded files" -ForegroundColor cyan -BackgroundColor black
Get-ChildItem . -Include *.pgy -File -Recurse | foreach { Remove-Item -Path $_.FullName }

Write-Host "    Removing decoded files" -ForegroundColor cyan -BackgroundColor black
Get-ChildItem . -Include *.pgy-decoded -File -Recurse | foreach { Remove-Item -Path $_.FullName }

Write-Host "    Removing codebook files" -ForegroundColor cyan -BackgroundColor black
Get-ChildItem encodings/ -Include *.json -File -Recurse | foreach { Remove-Item -Path $_.FullName }

Write-Host "    Cleaning unit test files" -ForegroundColor cyan -BackgroundColor black
$FileName = "test/unit-tests/ut_pigeon.py"
if (Test-Path $FileName) {
  Remove-Item $FileName
}

Get-ChildItem test/unit-tests/ -Include *.json -File -Recurse | foreach { Remove-Item -Path $_.FullName }
Get-ChildItem test/unit-tests/ -Include *.test-output -File -Recurse | foreach { Remove-Item -Path $_.FullName }
