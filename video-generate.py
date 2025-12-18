import re
from datetime import datetime
from typing import Literal

from openai import OpenAI
import sys
import time
from pathlib import Path

ModelType = Literal["sora-2", "sora-2-pro", "sora-2-2025-10-06", "sora-2-pro-2025-10-06", "sora-2-2025-12-08"]
model: ModelType = "sora-2"
ImageSize = Literal["720x1280", "1280x720", "1024x1792", "1792x1024"]
image_size: ImageSize = "720x1280"


openai = OpenAI()

prompt = Path("video-generate-prompt.txt").read_text()
video = openai.videos.create(
    model=model,
    prompt=prompt,
    seconds="8",
    size=image_size,
)

print("Video generation started:", video)

progress = getattr(video, "progress", 0)
bar_length = 30

while video.status in ("in_progress", "queued"):
    # Refresh status
    video = openai.videos.retrieve(video.id)
    progress = getattr(video, "progress", 0)

    filled_length = int((progress / 100) * bar_length)
    bar = "=" * filled_length + "-" * (bar_length - filled_length)
    status_text = "Queued" if video.status == "queued" else "Processing"

    sys.stdout.write(f"\n{status_text}: [{bar}] {progress:.1f}%")
    sys.stdout.flush()
    time.sleep(2)

# Move to next line after progress loop
sys.stdout.write("\n")

date_str = re.sub(re.compile(r"\D+"), "_", datetime.now().isoformat())

with open(f"{date_str}_prompt.txt", "w") as f:
    f.write(prompt)
    f.write("\n")
    f.write(model)
    f.write("\n")
    f.write(image_size)

if video.status == "failed":
    message = getattr(
        getattr(video, "error", None), "message", "Video generation failed"
    )
    print(message)
else:
    print("Video generation completed:", video)
    print("Downloading video content...")

    content = openai.videos.download_content(video.id, variant="video")
    content.write_to_file(f"{date_str}_generated_video.mp4")

    print(f"Wrote {date_str}.mp4")
