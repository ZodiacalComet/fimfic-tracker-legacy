import os
import sys
from pathlib import Path

from .constants import DOWNLOAD_URL_BY_FORMAT, VALID_ECHO_COLORS


class ConfigValue:
    def __init__(self, *, name: str, valid_types, valid_values: list = None):
        self.name = name
        self.valid_types = valid_types
        self.valid_values = valid_values

    def validate(self, value, filepath):
        if not isinstance(value, self.valid_types):
            expected_types = (
                " or ".join(map(lambda t: repr(t.__name__), self.valid_types))
                if isinstance(self.valid_types, tuple)
                else repr(self.valid_types.__name__)
            )

            raise ValueError(
                '{0} expected value of type {1} but got {2} from the settings file "{3}".'.format(
                    self.name, expected_types, repr(type(value).__name__), filepath
                )
            )

        if self.valid_values is not None and value not in self.valid_values:
            raise ValueError(
                '{0} on settings file "{1}" can only be one of the following: {2}.'.format(
                    self.name, filepath, ", ".join(map(repr, self.valid_values))
                )
            )


CONFIG_VALUES = [
    ConfigValue(name="download_dir", valid_types=Path),
    ConfigValue(name="tracker_file", valid_types=Path),
    ConfigValue(
        name="download_format",
        valid_types=str,
        valid_values=DOWNLOAD_URL_BY_FORMAT.keys(),
    ),
    ConfigValue(name="download_delay", valid_types=(int, float)),
    ConfigValue(name="download_alt", valid_types=list),
    ConfigValue(name="download_alt_quiet", valid_types=bool),
]

CONFIG_VALUES.extend(
    [
        ConfigValue(name=name, valid_types=str, valid_values=VALID_ECHO_COLORS)
        for name in (
            "info_fg_color",
            "success_fg_color",
            "error_fg_color",
            "confirm_fg_color",
            "highlight_text_color",
            "highlight_number_color",
            "highlight_other_color",
        )
    ]
)


def import_config(filepath: Path) -> dict:
    """Import a python configuration file and return a dictionary of the
    configuration values.

    Arguments:
        filepath {Path} -- Path to the python configuration file.

    Returns:
        dict -- Mapping of the configuration values obtained from
        filepath.
    """
    name, ext = os.path.splitext(filepath.name)

    if not ext == ".py":
        raise ValueError(
            f'Configuration file "{filepath}" should have the ".py" extension.'
        )

    # TODO: Raise any other expection with filepath to the config from where it
    # came from.
    try:
        sys.path.insert(0, str(filepath.parent))
        config = __import__(name)
    except ModuleNotFoundError:
        raise ValueError(f'The configuration file "{filepath}" doesn\'t exist.')

    config = vars(config)
    parsed_config = {}

    for config_value in CONFIG_VALUES:
        name = config_value.name

        value = config.get(name, None)
        if value is None:
            continue

        config_value.validate(value, filepath)
        parsed_config[name] = value

    return parsed_config


def load_config(config_path_list: list) -> dict:
    """Load the given list of paths in order of reverse priority, where the
    values get overwritten by any other before them if defined, and returns
    the resulting configuration.

    Arguments:
        config_path_list {List[Path]} -- List of paths to python configuration
        files.

    Returns:
        dict -- Resulting mapping of the configuration.
    """
    config = {}

    for filepath in filter(lambda p: p.exists(), config_path_list):
        config.update(**import_config(filepath))

    return config
