from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from openai import OpenAI
import base64
import re
from datetime import datetime

Size = Literal["auto", "1024x1024", "1536x1024", "1024x1536", "256x256", "512x512", "1792x1024", "1024x1792"]
ModelType = Literal["dall-e-2", "dall-e-3", "gpt-image-1", "gpt-image-1-mini"]
QualityType = Literal["standard", "low", "medium", "high", "auto"]

@dataclass(frozen=True)
class Cost:
    model: ModelType
    quality: QualityType | None

COSTS_25_CENTS = Cost(model="gpt-image-1", quality="high")
COSTS_4_CENTS = Cost(model="gpt-image-1", quality="medium")
COSTS_1_CENTS = Cost(model="gpt-image-1", quality="low")

client = OpenAI()

# make a file called image-modify-prompt.txt if you haven't already and put your prompt in it
prompt = Path("image-modify-prompt.txt").read_text()

# put what kind of price you want to spend
COST_CHOICE: Cost = COSTS_4_CENTS
with open("image.jpg", "rb") as f:
    response = client.images.edit(
        model=COST_CHOICE.model,
        image=f,          # pass the file object directly
        prompt=prompt,
        size="1536x1024",
        quality=COST_CHOICE.quality,
    )

date_str = re.sub(re.compile(r"\D+"), "_", datetime.now().isoformat())

with open(f"{date_str}_prompt.txt", "w") as f:
    f.write(prompt)
    f.write("\n")
    f.write(COST_CHOICE.model)
    if COST_CHOICE.quality:
        f.write(" -- ")
        f.write(COST_CHOICE.quality)

image_data = response.data[0].b64_json
filename = f"{date_str}_modified_image.png"
with open(filename, "wb") as out:
    out.write(base64.b64decode(image_data))
print(f"Image saved as: \n{filename}")
