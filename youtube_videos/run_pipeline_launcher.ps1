# PowerShell launcher for YouTube pipeline
# 避免 && 语法错误

$ErrorActionPreference = "Stop"

try {
    # 切换到工作目录
    Set-Location "C:\Users\11132\.qclaw\workspace-yw3plsutb1jupnif\youtube_videos"
    
    # 执行流水线
    python run_pipeline.py
    
    Write-Host "Pipeline completed with exit code: $LASTEXITCODE"
    exit $LASTEXITCODE
}
catch {
    Write-Error "Pipeline failed: $_"
    exit 1
}
