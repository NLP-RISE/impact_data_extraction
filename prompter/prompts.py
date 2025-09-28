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
NULL_CLAUSE: str = (
    "If the information is not available in the content and table files, return the string 'NULL' to indicate that this information is missing."
)


## Prompts
LOCATION_PROMPT: str = (
    f"The location in which the event occurred. Use the official name of the area if available. {NULL_CLAUSE}"
)
LOCATION_SOURCE_PROMPT: str = (
    f"Specify the index number where you found information showing the location of this event for each of the locations found. {SOURCE_EXAMLE} {NULL_CLAUSE}"
)
INJURED_PROMPT: str = (
    f"Some number (such as '700' or 'three thousand') or range (such as 'between 12 and 18') or phrase (such as 'thousands of people') that represents the number of people who were harmed, injured, or hospitalized due to the event. This number doesn't include people who died. there are any words that describe or modify the number, include them as well, so if the sentence says 'At most 14 were injured.', then return 'at most 14'.  {NULL_CLAUSE}"
)
INJURED_SOURCE_PROMPT: str = (
    f"Specify the index number where you found information showing the number of injured people in this events for each of the injury instances found. {SOURCE_EXAMLE} {NULL_CLAUSE}"
)
DEATHS_PROMPT: str = (
    f"Some number (such as '700' or 'three thousand') or range (such as 'between 12 and 18') or phrase (such as 'thousands of people') that represents the number of people who were killed due to the event for each of the death instances found. If there are any words that describe or modify the number, include them as well, so if the sentence says 'At least 200 were killed.', then return 'at least 200'. {NULL_CLAUSE}"
)
DEATHS_SOURCE_PROMPT: str = (
    f"Specify the collection followed by the index number where you found information showing the number of dead people in this events. {SOURCE_EXAMLE} {NULL_CLAUSE}"
)
MAIN_EVENT_PROMPT: str = "Choose the type of the main event."
