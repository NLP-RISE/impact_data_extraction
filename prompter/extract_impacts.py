from outformer import Jsonformer, highlight_values
from transformers import AutoModelForCausalLM, AutoTokenizer
from torch import float16
import os
import pandas as pd

# Initialize model and tokenizer
model_name = "mistralai/Mixtral-8x7B-Instruct-v0.1"
model = AutoModelForCausalLM.from_pretrained(
    model_name, device_map="balanced", top_k=10, do_sample=True, torch_dtype=float16
)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Create Jsonformer instance
jsonformer = Jsonformer(model, tokenizer, max_tokens_string=200, debug=True)

event_list_json_schema = {
    "type": "object",
    "properties": {
        "events": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "properties": {
                    "Main_Event": {
                        "type": "string",
                        "enum": [
                            "Flood",
                            "Extratropical Storm/Cyclone",
                            "Tropical Storm/Cyclone",
                            "Extreme Temperature",
                            "Drought",
                            "Wildfire",
                            "Tornado",
                        ],
                        "description": "Choose the type of the main event.",
                    },
                    "Location": {
                        "type": "array",
                        "minItems": 1,
                        "items": {"type": "string"},
                        "description": "The location in which the event occurred. Use the official name of the area if available.",
                    },
                    "Location_source": {
                        "type": "array",
                        "minItems": 1,
                        "items": {"type": "string"},
                        "description": "Specify the row number where you found information showing the location of this event.",
                    },
                    "Injured": {
                        "type": "string",
                        "description": "Some number or range that represents the number of people who were harmed, injured, or hospitalized due to the event. This number doesn't include people who died. Example: 'at least 200'",
                    },
                    "Injured_source": {
                        "type": "string",
                        "description": "Specify the row number where you found information showing the number of injured people in this events",
                    },
                    "Deaths": {
                        "type": "string",
                        "description": "Some number or range that represents the number of people who were killed due to the event. Example: 'more than 4'",
                    },
                    "Deaths_source": {
                        "type": "string",
                        "description": "Specify the row number where you found information showing the number of dead people in this events'",
                    },
                },
            },
        }
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
        text += f"{filename}\n{content}\n-------------------\n"


prompt = f"Extract all incidents of deaths and injuries as well as the location that occured due to the n atural disaster {event_name}. Be accurate and return answers verbatim. Extract the answers ONLY using the text below:\n{text}"

generated_data = jsonformer.generate(
    schema=event_list_json_schema, prompt=prompt, temperature=0.25, max_attempts=10
)

# Highlight generated values
highlight_values(generated_data)
