Write-Host "Running tests" -ForegroundColor yellow -BackgroundColor black


Write-Host "Setting up test data" -ForegroundColor magenta -BackgroundColor black

$testFiles = @(
  @("test/data/basic.txt", "test/data/basic.pgy"),
  @("test/data/basic-no-extension", "test/data/basic-no-extension.pgy"),
  @("test/data/empty.x.y.z", "test/data/empty.x.y.z.pgy"),
  @("test/data/nippon.png", "test/data/japan.pgy")
  # run faster for now
)

$unitTestFiles = @(
  "test/unit-tests/SymbolNodeUnitTests.py"
)

Copy-Item "pigeon.py" -Destination "test/unit-tests/ut_pigeon.py"


Write-Host "Unit tests" -ForegroundColor magenta -BackgroundColor black

Foreach ($unitTest in $unitTestFiles)
{
  python $unitTest
  if( -not $? )
  {
    Write-Host "Unit test(s) failed. Exiting." -ForegroundColor red -BackgroundColor black
    exit
  }
}


Write-Host "Encoding files" -ForegroundColor magenta -BackgroundColor black

Foreach ($pair in $testFiles)
{
  $fin = $pair[0]
  $fout = $pair[1]
  Write-Host "    $fin" -ForegroundColor cyan -BackgroundColor black
  python pigeon.py encode --fin $fin --fout $fout
  if( -not $? )
  {
    Write-Host "Failed to encode $fin. Exiting." -ForegroundColor red -BackgroundColor black
    exit
  }
}


Write-Host "Encoding file with input stream" -ForegroundColor magenta -BackgroundColor black
$fin = $testFiles[0][0]
Write-Host "    $fin" -ForegroundColor cyan -BackgroundColor black
Get-Content $fin | python pigeon.py encode
if( -not $? )
{
  Write-Host "Failed to encode $fin. Exiting." -ForegroundColor red -BackgroundColor black
  exit
}


Write-Host "Encoding file multiple times with input stream" -ForegroundColor magenta -BackgroundColor black
$fin = $testFiles[0][0]
Write-Host "    $fin" -ForegroundColor cyan -BackgroundColor black
Get-Content $fin | python pigeon.py encode
Get-Content $fin | python pigeon.py encode
if( -not $? )
{
  Write-Host "Failed to encode $fin. Exiting." -ForegroundColor red -BackgroundColor black
  exit
}


Write-Host "Decoding files" -ForegroundColor magenta -BackgroundColor black

Foreach ($pair in $testFiles)
{
  $fin = $pair[1]
  $fout = $pair[0]+".pgy-decoded"
  Write-Host "    $fin" -ForegroundColor cyan -BackgroundColor black
  python pigeon.py decode --fin $fin --fout $fout
  if( -not $? )
  {
    Write-Host "Failed to decode $fin. Exiting." -ForegroundColor red -BackgroundColor black
    exit
  }
}


Write-Host "Checking decoded files match" -ForegroundColor magenta -BackgroundColor black

Foreach ($pair in $testFiles)
{
  $foriginal = $pair[0]
  $fdecoded = $pair[0]+".pgy-decoded"
  Write-Host "    $foriginal and $fdecoded" -ForegroundColor cyan -BackgroundColor black
  python test/data/files-match.py $foriginal $fdecoded
  if( -not $? )
  {
    Write-Host "Files do not match. Exiting." -ForegroundColor red -BackgroundColor black
    exit
  }
}

Write-Host "Finished tests" -ForegroundColor green -BackgroundColor black
