./clean.ps1

$testFiles = @(
  @("test/data/basic.txt", "test/data/basic.pgy"),
  @("test/data/basic-no-extension", "test/data/basic-no-extension.pgy"),
  @("test/data/empty.x.y.z", "test/data/empty.x.y.z.pgy")
  # run faster for now @("test/data/nippon.png", "test/data/japan.pgy")
)

Write-Host "Encoding files" -ForegroundColor green -BackgroundColor black

Foreach ($pair in $testFiles)
{
  $fin = $pair[0]
  $fout = $pair[1]
  Write-Host "    $fin" -ForegroundColor cyan -BackgroundColor black
  python pigeon.py encode --filein $fin --fileout $fout
  if( -not $? )
  {
    Write-Host "Failed to encode $fin. Exiting." -ForegroundColor red -BackgroundColor black
    exit
  }
}

Write-Host "Encoding file with input stream" -ForegroundColor green -BackgroundColor black
$fin = $testFiles[0][0]
Write-Host "    $fin" -ForegroundColor cyan -BackgroundColor black
Get-Content $fin | python pigeon.py encode
if( -not $? )
{
  Write-Host "Failed to encode $fin. Exiting." -ForegroundColor red -BackgroundColor black
  exit
}

Write-Host "Encoding file multiple times with input stream" -ForegroundColor green -BackgroundColor black
$fin = $testFiles[0][0]
Write-Host "    $fin" -ForegroundColor cyan -BackgroundColor black
Get-Content $fin | python pigeon.py encode
Get-Content $fin | python pigeon.py encode
if( -not $? )
{
  Write-Host "Failed to encode $fin. Exiting." -ForegroundColor red -BackgroundColor black
  exit
}

Write-Host "Decoding files" -ForegroundColor green -BackgroundColor black

Foreach ($pair in $testFiles)
{
  $fin = $pair[1]
  $fout = $pair[0]+".pgy-decoded"
  Write-Host "    $fin" -ForegroundColor cyan -BackgroundColor black
  python pigeon.py decode --filein $fin --fileout $fout
  if( -not $? )
  {
    Write-Host "Failed to decode $fin. Exiting." -ForegroundColor red -BackgroundColor black
    exit
  }
}
