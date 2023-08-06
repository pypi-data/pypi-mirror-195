from pydantic import validate_arguments
from pyfilter import FromList
import httpx

class Localization:
    @validate_arguments
    def __init__(self, language: str) -> None:
        self.__endpoint_url = f"https://sp-translations.socialpointgames.com/deploy/dc/android/prod/dc_android_{language}_prod_wetd46pWuR8J5CmS.json"
        self.__localization = self.__fetch()
        self.__localization_dict = FromList(self.__localization).join_keys_of_child_dicts_in_a_new_dict()

    def __fetch(self) -> list[dict]:
        response = httpx.get(self.__endpoint_url)
        data = response.json()
        return data

    @validate_arguments
    @classmethod
    def load(cls, loc: list[dict]):
        cls.__localization = loc
        cls.__localization_dict = FromList(loc).join_keys_of_child_dicts_in_a_new_dict()

        return cls

    @validate_arguments
    @classmethod
    def load_dict(cls, loc: dict):
        cls.__localization_dict = loc
        cls.__localization = {}

        for key, value in loc.items():
            cls.__localization[key] = value

        return cls

    @validate_arguments
    @classmethod
    def get_value_from_key(cls, key: str) -> str | None:
        if key in cls.__localization_dict.keys():
            return cls.__localization_dict[key]

    @validate_arguments
    @classmethod
    def get_key_from_value(cls, value: str) -> str | None:
        for dict_key, dict_value in cls.__localization_dict.items():
            if dict_value == value:
                return dict_key

    @validate_arguments
    @classmethod
    def get_dragon_name(cls, id: int) -> str | None:
        key = f"tid_unit_{id}_name"
        return cls.get_value_from_key(key)

    @validate_arguments
    @classmethod
    def get_dragon_description(cls, id: int) -> str | None:
        key = f"tid_unit_{id}_description"
        return cls.get_value_from_key(key)

    @validate_arguments
    @classmethod
    def get_attack_name(cls, id: int) -> str | None:
        key = f"tid_attack_name_{id}"
        return cls.get_value_from_key(key)

    @validate_arguments
    @classmethod
    def get_skill_name(cls, id: int) -> str | None:
        key = f"tid_skill_name_{id}"
        return cls.get_value_from_key(key)

    @validate_arguments
    @classmethod
    def get_skill_description(cls, id: int) -> str | None:
        key = f"tid_skill_description_{id}"
        return cls.get_value_from_key(key)

    @validate_arguments
    @classmethod
    def search_keys(cls, query: str) -> list[str] | list:
        query = (query
            .lower()
            .strip())

        results = []

        for key in cls.__localization_dict.keys():
            parsed_key = (key
                .lower()
                .strip())

            if query in parsed_key:
                results.append(key)

        return results

    @validate_arguments
    @classmethod
    def search_values(cls, query: str) -> list[str] | list:
        query = (query
            .lower()
            .strip())

        results = []

        for value in cls.__localization_dict.values():
            parsed_value = (value
                .lower()
                .strip())

            if query in parsed_value:
                results.append(value)

        return results

    @validate_arguments
    @classmethod
    def compare(cls, old_localization: dict | list) -> dict[str, list]:
        if type(old_localization) == list:
            old_localization = FromList(old_localization).join_keys_of_child_dicts_in_a_new_dict()

        new_fields = []
        edited_fields = []

        old_localization_keys = old_localization.keys()
        for key in cls.__localization_dict.keys():
            if key not in old_localization_keys:
                new_fields.append({
                    "key": key,
                    "value": cls.__localization_dict[key]
                })

        for key in old_localization_keys:
            if old_localization[key] != cls.__localization_dict[key]:
                edited_fields.append({
                    "key": key,
                    "old_value": old_localization[key],
                    "new_value": cls.__localization_dict[key]
                })

        return dict(
            new_fields = new_fields,
            edited_fields = edited_fields
        )

    @classmethod
    def get(cls):
        return cls.__localization

    @classmethod
    def get_dict(cls):
        return cls.__localization_dict

__all__ = [ Localization ]