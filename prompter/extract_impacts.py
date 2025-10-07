from outformer import Jsonformer, highlight_values
from transformers import AutoModelForCausalLM, AutoTokenizer
from torch import float16
import os
import pandas as pd
from prompts import (
    LOCATION_PROMPT,
    LOCATION_SOURCE_PROMPT,
    INJURED_PROMPT,
    INJURED_SOURCE_PROMPT,
    DEATHS_PROMPT,
    DEATHS_SOURCE_PROMPT,
    MAIN_EVENT_PROMPT,
    MAIN_EVENT_CATEGORIES,
)

# Initialize model and tokenizer
model_name = "mistralai/Mixtral-8x7B-Instruct-v0.1"
model = AutoModelForCausalLM.from_pretrained(
    model_name, device_map="balanced", top_k=10, do_sample=True, torch_dtype=float16
)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Create Jsonformer instance
jsonformer = Jsonformer(model, tokenizer, max_tokens_string=200, debug=False)

event_list_json_schema = {
    "type": "object",
    "properties": {
        "events": {
            "type": "array",
            "minItems": 2,
            "items": {
                "type": "object",
                "properties": {
                    "Main_Event": {
                        "type": "string",
                        "enum": MAIN_EVENT_CATEGORIES,
                        "description": MAIN_EVENT_PROMPT,
                    },
                    # treat this as a single object to enforce proper completion where each location/impact has a source
                    "Location_block": {
                        "type": "array",
                        "minItems": 1,
                        "items": {
                            "type": "object",
                            "properties": {
                                "Location": {
                                    "type": "string",
                                    "description": LOCATION_PROMPT,
                                },
                                "Location_source": {
                                    "type": "string",
                                    "description": LOCATION_SOURCE_PROMPT,
                                },
                            },
                        },
                    },
                    "Deaths_block": {
                        "type": "array",
                        "minItems": 1,
                        "items": {
                            "type": "object",
                            "properties": {
                                "Deaths": {
                                    "type": "string",
                                    "description": DEATHS_PROMPT,
                                },
                                "Deaths_source": {
                                    "type": "string",
                                    "description": DEATHS_SOURCE_PROMPT,
                                },
                            },
                        },
                    },
                    "Injured_block": {
                        "type": "array",
                        "minItems": 1,
                        "items": {
                            "type": "object",
                            "properties": {
                                "Injured": {
                                    "type": "string",
                                    "description": INJURED_PROMPT,
                                },
                                "Injured_source": {
                                    "type": "string",
                                    "description": INJURED_SOURCE_PROMPT,
                                },
                            },
                        },
                    },
                },
            },
        },
    },
}

event_dir = "articles/text"
event_name = "1922 Shantou typhoon"
event_files = sorted(
    [f"{event_dir}/{event_name}/{i}" for i in os.listdir(f"{event_dir}/{event_name}")]
)

text = ""

for file in event_files:
    filename = file.split("/")[-1].replace(".csv", "")
    with open(file, "r") as content_file:
        content = content_file.read()

        text += f"Event name: {event_name}\nCollection: {filename}\n\n{content}\n-------------------\n"

prompt = f"Extract all incidents of deaths and injuries as well as the location that occured due to the natural disaster {event_name}. Be accurate and return answers verbatim. Extract the answers ONLY using the text below:\n{text}"
print(prompt)

generated_data = jsonformer.generate(
    schema=event_list_json_schema, prompt=prompt, temperature=0.25, max_attempts=10
)

# Highlight generated values
highlight_values(generated_data)
