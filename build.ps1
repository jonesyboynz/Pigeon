Write-Host "Running build" -ForegroundColor yellow -BackgroundColor black

Write-Host "    Building codebook files" -ForegroundColor cyan -BackgroundColor black
cd encodings
python generate-basic.py
python generate-numeric.py
cd ..

Write-Host "Finished build" -ForegroundColor green -BackgroundColor black
