#!/usr/bin/bash
# Monitor youtube_videos for new .html files and upload to GitHub repo
# Called by Claude cron job every 30 minutes

SOURCE_DIR="C:/Users/11132/.qclaw/workspace-yw3plsutb1jupnif/youtube_videos"
REPO_DIR="D:/code_projects/vibecoding/yzwer.github.io"
TARGET_DIR="$REPO_DIR/static/youtube-articles"
STATE_FILE="$REPO_DIR/.claude/uploaded_files.txt"
COMMIT_LOG="$REPO_DIR/.claude/upload_log.txt"

# Ensure target directory exists
mkdir -p "$TARGET_DIR"

# Find all .html files in source dir (recursive)
new_files=()
total=0
uploaded=0

while IFS= read -r -d '' file; do
    basename=$(basename "$file")
    total=$((total + 1))

    # Check if already uploaded (state file)
    if [ -f "$STATE_FILE" ] && grep -Fxq "$basename" "$STATE_FILE"; then
        continue
    fi

    # New file found
    new_files+=("$file")
    cp "$file" "$TARGET_DIR/$basename"
    echo "$basename" >> "$STATE_FILE"
    uploaded=$((uploaded + 1))
done < <(find "$SOURCE_DIR" -name "*.html" -type f -print0 2>/dev/null)

# If no new files, done
if [ "$uploaded" -eq 0 ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] No new files. ($total total, 0 new)"
    # Keep state file sorted and unique
    [ -f "$STATE_FILE" ] && sort -u -o "$STATE_FILE" "$STATE_FILE"
    exit 0
fi

# Keep state file sorted and unique
sort -u -o "$STATE_FILE" "$STATE_FILE"

# Commit and push to GitHub
cd "$REPO_DIR" || exit 1

# Git add new files and state
for file in "${new_files[@]}"; do
    basename=$(basename "$file")
    git add "static/youtube-articles/$basename"
done
git add "$STATE_FILE"

# Build commit message with filenames
names=""
for file in "${new_files[@]}"; do
    basename=$(basename "$file")
    names="$names $basename"
done

git commit -m "auto: upload$names" --no-verify 2>&1 >> "$COMMIT_LOG"

# Push
if git push origin master 2>&1 >> "$COMMIT_LOG"; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Uploaded $uploaded new file(s):${names}"
else
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Push failed for $uploaded file(s)"
fi
