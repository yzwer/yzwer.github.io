$dir = 'C:\Users\11132\.qclaw\workspace-yw3plsutb1jupnif\youtube_videos'
Set-Location $dir

$readme = 'README_UPLOAD.txt'
$htmlFiles = Get-ChildItem '*_wechat_article.html' | Select-Object -ExpandProperty Name
$allFiles = @($readme) + $htmlFiles

Write-Host "Packing $($allFiles.Count) files..."
Compress-Archive -Path $allFiles -DestinationPath 'articles_backup.zip' -Force

$zip = Get-Item 'articles_backup.zip'
$sizeMB = [math]::Round($zip.Length / 1MB, 2)
Write-Host "Done: articles_backup.zip ($sizeMB MB)"
Write-Host "Location: $dir\articles_backup.zip"
