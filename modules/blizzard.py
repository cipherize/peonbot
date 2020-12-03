from modules.config import config
from wowapi import WowApi

api = WowApi(config.blizzard.api.id, config.blizzard.api.secret)

data = api.get_realm_index("us", "dynamic-us", locale="en_US")
realm_name_to_slug = {r["name"].lower(): r["slug"] for r in data["realms"]}
realm_slug_to_name = {r["slug"]: r["name"] for r in data["realms"]}
del data


def get_realm_name(realm_slug: str) -> str:
    if realm_slug in realm_slug_to_name:
        return realm_slug_to_name[realm_slug]
    else:
        return None


def get_realm_slug(realm_name: str) -> str:
    if realm_name.lower() in realm_name_to_slug:
        return realm_name_to_slug[realm_name.lower()]
    else:
        return None


def get_equipment_summary(char_name: str, realm_name: str) -> list:

    realm_slug = realm_name_to_slug[realm_name]
    char_name = char_name.lower()

    data = api.get_character_equipment_summary(
        "us", "profile-us", realm_slug, char_name, locale="en_US"
    )

    return data["equipped_items"]
