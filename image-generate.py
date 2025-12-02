import base64
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Any

from openai import OpenAI
from datetime import datetime

Size = Literal["auto", "1024x1024", "1536x1024", "1024x1536", "256x256", "512x512", "1792x1024", "1024x1792"]
ModelType = Literal["dall-e-2", "dall-e-3", "gpt-image-1", "gpt-image-1-mini"]
QualityType = Literal["standard", "hd", "low", "medium", "high", "auto"]

@dataclass(frozen=True)
class Cost:
    model: ModelType
    quality: QualityType | None

COSTS_25_CENTS = Cost(model="gpt-image-1", quality="high")
COSTS_4_CENTS = Cost(model="gpt-image-1", quality="medium")
COSTS_1_CENTS = Cost(model="gpt-image-1", quality="low")
COSTS_4_CENTS_DALL_E = Cost(model="dall-e-3", quality="hd")
COSTS_2_CENTS_DALL_E = Cost(model="dall-e-2", quality=None)

client = OpenAI()

# make a file called image-generate-prompt.txt if you haven't already and put your prompt in it
prompt = Path("image-generate-prompt.txt").read_text()

# put what kind of price you want to spend
COST_CHOICE: Cost = COSTS_1_CENTS
image_gen_args: dict[str, Any] = {
    "model": COST_CHOICE.model,
    "prompt": prompt,
    "size": "1024x1024",
}
if image_gen_args["model"] != COSTS_2_CENTS_DALL_E.model:
    image_gen_args["quality"] = COST_CHOICE.quality

# this generates the image
response = client.images.generate(**image_gen_args)

date_str = re.sub(re.compile(r"\D+"), "_", datetime.now().isoformat())

with open(f"{date_str}_prompt.txt", "w") as f:
    f.write(prompt)
    f.write("\n")
    f.write(COST_CHOICE.model)
    if COST_CHOICE.quality:
        f.write(" -- ")
        f.write(COST_CHOICE.quality)

url_value = response.data[0].url

if url_value:
    print(f"Image available at: \n{response.data[0].url}")
    with open(f"{date_str}_url.txt", "w") as f:
        f.write(url_value)
else:
    image_bytes = base64.b64decode(response.data[0].b64_json)
    filename = f"{date_str}_generated_image.png"
    with open(filename, "wb") as f:
        f.write(image_bytes)
    print(f"Image saved as: \n{filename}")