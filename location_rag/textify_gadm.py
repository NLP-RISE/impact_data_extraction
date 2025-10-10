import pandas as pd
from tqdm import tqdm


tqdm.pandas()


def textify(row):
    text = ""

    if not pd.isna(row["NAME_5"]):
        text += f'{row["NAME_5"]} (GID: {row["GID_5"]}) is an area located in {row["NAME_4"]} (GID: {row["GID_4"]}). '

    if not pd.isna(row["NAME_4"]):
        if not pd.isna(row["VARNAME_4"]):
            text += f'{row["NAME_4"]} (GID: {row["GID_4"]}) (also known by other names as: {", ".join(row["VARNAME_4"].split("|"))}) is an area located in {row["NAME_3"]} (GID: {row["GID_3"]}).'
        else:
            text += f'{row["NAME_4"]} (GID: {row["GID_4"]}) is an area located in {row["NAME_3"]} (GID: {row["GID_3"]}). '

    if not pd.isna(row["NAME_3"]):
        if not pd.isna(row["VARNAME_3"]):
            text += f'{row["NAME_3"]} (GID: {row["GID_3"]}) (also known by other names as: {", ".join(row["VARNAME_3"].split("|"))}) is an area located in {row["NAME_2"]} (GID: {row["GID_2"]}). '

        else:
            text += f'{row["NAME_3"]} (GID: {row["GID_3"]}) is an area located in {row["NAME_2"]} (GID: {row["GID_2"]}). '

    if not pd.isna(row["NAME_2"]):
        if not pd.isna(row["VARNAME_2"]):
            text += f'{row["NAME_2"]} (GID: {row["GID_2"]}) (also known by other names as: {", ".join(row["VARNAME_2"].split("|"))}) is an area located in {row["NAME_1"]} (GID: {row["GID_1"]}). '
        else:
            text += f'{row["NAME_2"]} (GID: {row["GID_2"]}) is an area located in {row["NAME_1"]} (GID: {row["GID_1"]}). '

    if not pd.isna(row["NAME_1"]):
        if not pd.isna(row["VARNAME_1"]):
            text += f'{row["NAME_1"]} (GID: {row["GID_1"]}) (also known by other names as: {", ".join(row["VARNAME_1"].split("|"))}) is an area located in {row["NAME_0"]} (GID: {row["GID_0"]}). '
        else:
            text += f'{row["NAME_1"]} (GID: {row["GID_1"]}) is an area located in {row["NAME_0"]} (GID: {row["GID_0"]}). '

    if not pd.isna(row["NAME_0"]):
        if not pd.isna(row["VARNAME_0"]):
            text += f'{row["NAME_0"]} (also known by other names as: {", ".join(row["VARNAME_0"].split("|"))}) is a country with the following GID: {row["GID_0"]}. '
        else:
            text += (
                f'{row["NAME_0"]} is a country with the following GID: {row["GID_0"]}. '
            )

    if not pd.isna(row["CONTINENT"]):
        if not pd.isna(row["SUBCONT"]):
            text += f'{row["NAME_0"]} is also located in the subcontinent of {row["SUBCONT"]}, and in the continent of {row["CONTINENT"]}. '
        else:
            text += (
                f'{row["NAME_0"]} is located in the continent of {row["CONTINENT"]}. '
            )

    if not pd.isna(row["REGION"]):
        if not pd.isna(row["VARREGION"]):
            text += f'{row["NAME_0"]} is located in the {row["REGION"]} region (also known as {row["VARREGION"]}). '
        else:
            text += f'{row["NAME_0"]} is part of the {row["REGION"]} region. '

    if not pd.isna(row["GOVERNEDBY"]):
        text += f'{row["NAME_0"]} (GID: {row["GID_0"]}) is governed by {row["GOVERNEDBY"]} (GID: {get_gid_0(row["GOVERNEDBY"])}). '

    if not pd.isna(row["DISPUTEDBY"]):
        text += f'{row["NAME_0"]} (GID: {row["GID_0"]}) is disputed by {row["DISPUTEDBY"]} (GID: {get_gid_0(row["DISPUTEDBY"])}). '

    if not pd.isna(row["SOVEREIGN"]):
        text += f'{row["NAME_0"]} (GID: {row["GID_0"]}) is under the sovereignty of {row["SOVEREIGN"]} (GID: {get_gid_0(row["SOVEREIGN"])}). '

    return text


gadm = pd.read_csv(
    "data/gadm_world.csv",
)
gadm_chunked = pd.read_csv("data/gadm_world.csv", chunksize=1000)


def get_gid_0(name: str) -> str | None:
    """Returns a country GID by its name"""
    try:
        gid_0 = list(set(gadm.loc[gadm["NAME_0"] == name]["GID_0"]))
        assert len(gid_0) == 1
        return gid_0[0]
    except:
        return None


for i in tqdm(gadm_chunked, desc="chunks"):
    i["text"] = i.progress_apply(textify, axis=1)
    i["text"].to_csv("gadm_text.csv", index=False, mode="a")
