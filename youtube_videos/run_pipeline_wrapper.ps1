# PowerShell wrapper for run_pipeline.py
# 避免 && 语法错误

$WORK_DIR = "C:\Users\11132\.qclaw\workspace-yw3plsutb1jupnif\youtube_videos"

# 切换到工作目录
Set-Location -Path $WORK_DIR

# 执行Python脚本
python.exe "$WORK_DIR\run_pipeline.py"

# 返回退出码
exit $LASTEXITCODE
