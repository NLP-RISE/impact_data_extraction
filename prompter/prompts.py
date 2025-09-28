LOCATION_PROMPT: str = (
    "The location in which the event occurred. Use the official name of the area if available."
)
LOCATION_SOURCE_PROMPT: str = (
    "Specify the row number where you found information showing the location of this event."
)
INJURED_PROMPT: str = (
    "Some number or range that represents the number of people who were harmed, injured, or hospitalized due to the event. This number doesn't include people who died. Example: 'at least 200'"
)
INJURED_SOURCE_PROMPT: str = (
    "Specify the row number where you found information showing the number of injured people in this events"
)
DEATHS_PROMPT: str = (
    "Some number or range that represents the number of people who were killed due to the event. Example: 'more than 4'"
)
DEATHS_SOURCE_PROMPT: str = (
    "Specify the row number where you found information showing the number of dead people in this events'"
)
MAIN_EVENT_PROMPT: str = "Choose the type of the main event."
MAIN_EVENT_CATEGORIES: list = [
    "Flood",
    "Extratropical Storm/Cyclone",
    "Tropical Storm/Cyclone",
    "Extreme Temperature",
    "Drought",
    "Wildfire",
    "Tornado",
]
