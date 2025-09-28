## Blocks

SOURCE_EXAMLE: str = (
    "For example, return content_65 where content is the collection name and the number represents the index"
)
MAIN_EVENT_CATEGORIES: list = [
    "Flood",
    "Extratropical Storm/Cyclone",
    "Tropical Storm/Cyclone",
    "Extreme Temperature",
    "Drought",
    "Wildfire",
    "Tornado",
]

## Prompts
LOCATION_PROMPT: str = (
    "The location in which the event occurred. Use the official name of the area if available."
)
LOCATION_SOURCE_PROMPT: str = (
    f"Specify the index number where you found information showing the location of this event for each of the locations found. {SOURCE_EXAMLE}"
)
INJURED_PROMPT: str = (
    "Some number (such as '700' or 'three thousand') or range (such as 'between 12 and 18') or phrase (such as 'thousands of people') that represents the number of people who were harmed, injured, or hospitalized due to the event. This number doesn't include people who died. Example: 'at least 200'"
)
INJURED_SOURCE_PROMPT: str = (
    f"Specify the index number where you found information showing the number of injured people in this events for each of the injury instances found. {SOURCE_EXAMLE}"
)
DEATHS_PROMPT: str = (
    "Some number (such as '700' or 'three thousand') or range (such as 'between 12 and 18') or phrase (such as 'thousands of people') that represents the number of people who were killed due to the event for each of the death instances found. Example: 'more than 4'"
)
DEATHS_SOURCE_PROMPT: str = (
    f"Specify the collection followed by the index number where you found information showing the number of dead people in this events. {SOURCE_EXAMLE}"
)
MAIN_EVENT_PROMPT: str = "Choose the type of the main event."
