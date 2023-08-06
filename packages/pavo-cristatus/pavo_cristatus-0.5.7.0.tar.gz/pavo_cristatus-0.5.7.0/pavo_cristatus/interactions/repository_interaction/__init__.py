from collections import defaultdict
from typing import Any

from picidae import expand_parameter_list_by_x, false

from pavo_cristatus.interactions.repository_interaction import repository_interaction
from pavo_cristatus.interactions.repository_interaction.repository_interaction import RepositoryInteraction
from pavo_cristatus.dependency_injection.ploceidae_configurator import pavo_cristatus_dependency_wrapper
from pavo_cristatus.utilities import access_interaction_callable
from pavo_cristatus.interactions.repository_interaction import operations

__all__ = ["repository_interaction", "RepositoryInteraction"]

def sql_repository_write_interaction(sqlite_repository : Any) -> RepositoryInteraction:
    return RepositoryInteraction(sqlite_repository, expand_parameter_list_by_x(operations.write_data_item, 1), false)

def sql_repository_read_interaction(sqlite_repository : Any) -> RepositoryInteraction:
    return RepositoryInteraction(sqlite_repository, operations.read_data_item, lambda: defaultdict(dict))

pavo_cristatus_dependency_wrapper(transformation=access_interaction_callable)(sql_repository_write_interaction)
pavo_cristatus_dependency_wrapper(transformation=access_interaction_callable)(sql_repository_read_interaction)