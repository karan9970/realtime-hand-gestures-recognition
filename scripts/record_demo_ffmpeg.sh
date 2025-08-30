
#!/usr/bin/env bash
# Records a region of the screen for 15 seconds and saves to demo/demo.mp4.
# Adjust -video_size and -offset_x/y as needed.
# Requires: ffmpeg
DURATION="${1:-15}"
OUT="demo/demo.mp4"
echo "Recording $DURATION seconds to $OUT ..."
# This command is intentionally generic; users should edit it for their OS/FFmpeg build.
ffmpeg -y -f avfoundation -framerate 30 -i "0" -t "$DURATION" "$OUT"
echo "Done."
