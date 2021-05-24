./clean.ps1

Write-Host "Encoding files" -ForegroundColor green -BackgroundColor black

$testFiles = @(
  @("test/data/basic.txt", "test/data/basic.pgy"),
  @("test/data/basic-no-extension", "test/data/basic-no-extension.pgy"),
  @("test/data/empty", "test/data/empty.pgy")
)

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
