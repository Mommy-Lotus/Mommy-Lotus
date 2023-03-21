from typing import List

import toml


def get_attr(toml_dict: dict, section: str, attr_key: str):
    """
    Helper method for getting values from config override or config template.
    """
    try:
        return toml_dict[section][attr_key]
    except KeyError:
        return toml.load("config/config.template.toml", _dict=dict)[section][attr_key]


class Config:
    """
    Wrapper class for Config and config template.\n
    It checks value from config override and if not exists that will be take from config template.
    """

    toml_dict: dict = toml.load("config/config.toml", _dict=dict)

    # Authorization
    key: str = get_attr(toml_dict, "base", "key")

    # Base information
    admin_ids: List[int] = get_attr(toml_dict, "base", "admin_ids")
    guild_id: int = get_attr(toml_dict, "base", "guild_id")
    default_prefix: str = get_attr(toml_dict, "base", "default_prefix")

    # Special channel IDs
    bot_dev_channel: int = get_attr(toml_dict, "channels", "bot_dev_channel")
    bot_room: int = get_attr(toml_dict, "channels", "bot_room")


config = Config()


def load_config():
    global config
    config = Config()
