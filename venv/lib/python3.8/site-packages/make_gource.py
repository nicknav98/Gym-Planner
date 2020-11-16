import subprocess

proc = subprocess.call("gource --disable-progress --stop-at-end --output-ppm-stream - | ffmpeg -y -b 3000K -r 60 -f image2pipe -vcodec ppm -i - gource.avi", shell=True)
