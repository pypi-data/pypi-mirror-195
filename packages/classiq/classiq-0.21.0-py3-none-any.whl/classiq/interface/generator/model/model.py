from typing import Any, Dict, List

import pydantic

import classiq.interface.generator.validations.flow_graph as flow_graph
from classiq.interface.generator.function_call import SUFFIX_RANDOMIZER, FunctionCall
from classiq.interface.generator.functions import (
    FunctionLibraryData,
    update_standalone_logic_flow,
)
from classiq.interface.generator.model.constraints import Constraints
from classiq.interface.generator.model.preferences.preferences import Preferences
from classiq.interface.helpers.versioned_model import VersionedModel


class Model(VersionedModel):
    """
    All the relevant data for generating quantum circuit in one place.
    """

    # Must be validated before logic_flow
    function_library: FunctionLibraryData = pydantic.Field(
        default_factory=FunctionLibraryData,
        description="The user-defined custom function library.",
    )

    constraints: Constraints = pydantic.Field(default_factory=Constraints)
    preferences: Preferences = pydantic.Field(default_factory=Preferences)

    inputs: Dict[str, str] = pydantic.Field(
        default_factory=dict,
        description="A mapping between the name of an input and the name of the wire "
        "that connects to this input",
    )
    outputs: Dict[str, str] = pydantic.Field(
        default_factory=dict,
        description="A mapping between the name of an output and the name of the wire "
        "that connects to this output",
    )
    logic_flow: List[FunctionCall] = pydantic.Field(
        default_factory=list,
        description="List of function calls to be applied in the circuit",
    )

    @pydantic.validator("preferences", always=True)
    def _seed_suffix_randomizer(cls, preferences: Preferences) -> Preferences:
        SUFFIX_RANDOMIZER.seed(preferences.random_seed)
        return preferences

    @pydantic.validator("logic_flow")
    def validate_logic_flow(
        cls, logic_flow: List[FunctionCall], values: Dict[str, Any]
    ) -> List[FunctionCall]:
        library = values["function_library"]
        update_standalone_logic_flow(logic_flow, library.function_dict)
        for fd in library.function_dict.values():
            fd.update_logic_flow(library.function_dict)

        inputs: Dict[str, str] = values.get("inputs", dict())
        outputs: Dict[str, str] = values.get("outputs", dict())

        flow_graph.validate_legal_wiring(
            logic_flow,
            flow_input_names=list(inputs.values()),
            flow_output_names=list(outputs.values()),
        )
        flow_graph.validate_acyclic_logic_flow(
            logic_flow,
            flow_input_names=list(inputs.values()),
            flow_output_names=list(outputs.values()),
        )

        return logic_flow
