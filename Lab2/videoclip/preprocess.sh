#!/bin/zsh
echo "1. Separate audio from video..."
ffmpeg -i $1 -f mp3 -vn $2 -loglevel quiet
echo "2. Generate subtitle file..."
autosub -S zh-CN -D zh-CN $2