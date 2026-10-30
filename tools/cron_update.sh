#!/usr/bin/env bash
# Hourly: new/edited 執刑者 chapters -> MP3 -> RSS -> push (GitHub Pages; Spotify picks it up).
export HOME=/usr/local/google/home/linyuwei
export PATH="$HOME/.local/bin:/usr/local/bin:/usr/bin:/bin"
cd "$HOME/.gemini/jetski/scratch/zhixingzhe-podcast" || exit 1
exec 9>/tmp/zhixingzhe-podcast.lock
flock -n 9 || exit 0
{
  echo "=== $(date '+%F %T')"
  git pull -q --rebase || true
  python3 -u tools/batch.py && python3 tools/build_feed.py
  if [ -n "$(git status --porcelain)" ]; then
    git add -A && git commit -qm "有聲書自動更新 $(date '+%F %H:%M')" && git push -q && echo pushed
  fi
} >> "$HOME/.gemini/jetski/scratch/zhixingzhe-podcast/cron.log" 2>&1
