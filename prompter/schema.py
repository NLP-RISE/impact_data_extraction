event_list_json_schema = {
    "type": "object",
    "properties": {
        "events": {
            "type": "array",
            "minItems": 1,
            "items": {
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
                    "description": "",
                },
                "Location": {
                    "type": "array",
                    "minItems": 1,
                    "items": {"type": "string"},
                    "description": "The location in which the event occurred. Use the official name of the area if available.",
                },
                "Injured": {
                    "type": "string",
                    "description": "Some number or range that represents the number of people who were harmed, injured, or hospitalized due to the event. This number doesn't include people who died.",
                },
                "Deaths": {
                    "type": "string",
                    "description": "Some number or range that represents the number of people who were killed due to the event.",
                },
            },
        }
    },
}
