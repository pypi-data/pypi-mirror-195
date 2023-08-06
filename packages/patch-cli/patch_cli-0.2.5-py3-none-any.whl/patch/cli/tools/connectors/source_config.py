from abc import ABC, abstractmethod
from collections import deque
from typing import Optional, TextIO, Any, List

from patch.cli.tools.connectors.connector_spec import field_specs, ConnectorConfigSpec
from patch.cli.tools.field_spec import FieldSpec, FieldChoice
from patch.cli.tools.json_reader import read_json


def choices_to_gql_value(field_name: str, choices: List[FieldChoice], key_val: str) -> str:
    for choice in choices:
        if choice.key == key_val:
            return choice.gql_value
    accepted_choices = ", ".join([ch.key for ch in choices])
    raise SpecVerificationError(f"Unknown value for field: {field_name}. Accepted values: {accepted_choices}")


class SpecVerificationError(Exception):
    pass


class SourceConfig(ABC):
    """The source config.

    This class manages collecting and interpreting source configuration.
    There are two possible sources of the configuration:
    - configuration JSON file
    - the function resolve_missing_config_field from subclasses
               (for example, in the interactive subclass, it asks user for the value)
    """

    config: dict
    staging_db: Optional[str]

    def __init__(self, file_config: Optional[TextIO], staging_db: Optional[str]):
        self.config = read_json(file_config, SpecVerificationError)
        self.staging_db = staging_db

    @abstractmethod
    def resolve_missing_config_field(self, field: FieldSpec) -> Optional[Any]:
        """
        Called during `resolve_config`, once for each applicable field that was missing in the config file.
        If the value cannot be resolved, returns None.
        :return: The value of the field or None if the value cannot be resolved.
        """
        pass

    @abstractmethod
    def finalize_key_resolution(self) -> None:
        """
        Finalization function for field resolvers.
        For example, can say "thank you" to the user, or throws exception with all missing fields.
        """
        pass

    def resolve_config(self):
        """
        The function tries to resolve values for all fields from the specification.
        If values can't be resolved, it throws an exception.
        If there are excessive values, it throws an exception.
        :return:
        """
        input_values: dict = self.config.copy()
        result_values: dict = {}
        input_spec = deque(field_specs)
        while input_spec:
            field = input_spec.popleft()
            value = input_values.pop(field.key, None)
            if not value:
                value = self.resolve_missing_config_field(field)
            if field.choices is not None and value is not None:
                value = choices_to_gql_value(field.key, field.choices, value)
            result_values[field.key] = value
            if field.conditions:
                for condition in field.conditions:
                    if condition.if_value == value and condition.then_fields:
                        # Add new questions at the beginning of the list
                        input_spec.extendleft(condition.then_fields)
        self.finalize_key_resolution()
        if input_values:
            keys = list(input_values)
            if len(keys) == 1:
                raise SpecVerificationError(f"Unknown key: {keys[0]}")
            else:
                key_values = ", ".join(keys)
                raise SpecVerificationError(f"Unknown keys: {key_values}")
        return result_values

    def send_to_gql(self, patch_ctx, values: dict):
        client = patch_ctx.gql_client
        config = values.copy()
        connector_type = config.pop('type', None)
        connector_spec = ConnectorConfigSpec(connector_type)
        if self.staging_db:
            config['stagingDatabase'] = self.staging_db
        mut = client.prepare_mutation(connector_spec.mutation_name, input=config)
        return mut.execute()
