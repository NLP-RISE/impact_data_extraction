import pandas as pd
import shortuuid
from ast import literal_eval

def random_short_uuid(length: int = 7) -> str:
        """Generates a short alpha-numerical UID"""
        return shortuuid.ShortUUID().random(length=length)

if __name__ == "__main__":
    raw_annotations = pd.read_csv("annotations/annotations_raw.csv", keep_default_na=False)
    article_titles = pd.read_csv("annotations/articles.csv", index_col=None)
    article_map = {}
    for _, d in article_titles[["URL", "Title"]].iterrows():
        article_map[d["URL"]] = d["Title"]
    # print(article_titles.to_dict(orient=""))
    # todo: use _ID columns to get source of information
    
    target_columns = [
        "parent_event_id", 
        "main_event", 
        "sub_events",
        "UUID",
        "Event_ID_decimal",# decimal event id, to distinguish summary events from more finegrained information form the same "event"
        "Event_Type", # singe/multi
        "Main_Event", # event "type" -- flood, etc
        "Hazard", # hazard, categorical list
        "Source", # link to wikipedia article
        "Event_Name", # event name, either from title or article
        "Location", # using & and |
        "GID(s)", # list separated by |
        "Start_Year", 
        "Start_Month",
        "Start_Day",
        "End_Year",
        "End_Month",
        "End_Day",
        "Injured_Min",
        "Injured_Max",
        "Deaths_Min",
        "Deaths_Max",
        "Displaced_Min",
        "Displaced_Max",
        "Homelessness_Min",
        "Homelessness_Max",
        "Affected_Min",
        "Affected_Max",
        "Buildings_Damaged_Min",
        "Buildings_Damaged_Max",
        "Insured_Damage_Min",
        "Insured_Damage_Max",
        "Insured_Damage_Unit",
        "Insured_Damage_Inflation_Adjusted",
        "Insured_Damage_Inflation_Adjusted_Year",
        "Damage_Min",
        "Damage_Max",
        "Damage_Units",
        "Damage_Inflation_Adjusted",
        "Damage_Inflation_Adjusted_Year",
    ]
    raw_annotations = raw_annotations[raw_annotations["Annotation Code"].isin(["1", "2", "3", "4", "5"])]
    raw_annotations["Title"] = raw_annotations["Source"].map(article_map)
    raw_annotations["Hazard"] = raw_annotations["Hazard"].apply(lambda x: x.split("|"))
    raw_annotations["GID(s)"] = raw_annotations["GID(s)"].apply(lambda x: x.split("|"))
    raw_annotations["Location"] = raw_annotations["Location"].apply(lambda x: x.split("|")) # full location names are retained using &, better than replacing it with a comme ","
    raw_annotations["UUID"] = [random_short_uuid() for _ in raw_annotations.index]
    raw_annotations["level"] = raw_annotations["Event_ID_decimal"].apply(lambda x: "main" if ".00" in x else "sub")
    raw_annotations["parent_event_id"] = raw_annotations["Event_ID_decimal"].apply(lambda x: int(x.replace(",", "").split(".")[0]))
    sub_events = raw_annotations[["parent_event_id", "UUID", "level"]][raw_annotations["level"] == "sub"].groupby("parent_event_id").agg({'UUID': lambda x: list(x)})
    main_events = raw_annotations[["parent_event_id", "UUID", "level"]][raw_annotations["level"] == "main"].groupby("parent_event_id").agg({'UUID': lambda x: x})
    main_event = main_events.to_dict("dict")["UUID"]
    sub_events = sub_events.to_dict("dict")["UUID"]

    raw_annotations["sub_events"] = [[] for _ in raw_annotations.index]
    raw_annotations["main_event"] = [None for _ in raw_annotations.index]

    def find_events(row: dict):
        new_row = row.copy()
        if row["level"] == "main":
            if row["parent_event_id"] in sub_events.keys():
                new_row["sub_events"] = sub_events[row["parent_event_id"]]
        if row["level"] == "sub":
             if row["parent_event_id"] in sub_events.keys():
                  new_row["main_event"] = main_event[row["parent_event_id"]]
        return new_row
    
    output = raw_annotations.apply(find_events, axis=1)
    output[target_columns].to_csv("annotations/annotations_clean.csv")