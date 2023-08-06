import collections
import sys
from typing import Callable, Any

from pavo_cristatus.module_symbols import symbol_creator
from pavo_cristatus.module_symbols.abstract_symbol import AbstractSymbol
from pavo_cristatus.project_loader.nested_symbol_collector import collect_nested_symbols

__all__ = ["collect"]

from pavo_cristatus.project_loader.normalized_module_symbol import NormalizedModuleSymbol
from pavo_cristatus.project_loader.normalized_symbol import NormalizedSymbol


def convert_to_symbol_object(project_root_path, normalized_symbol, is_symbol_of_interest):
    """
    converts a python symbol to a Symbol object
    :param project_root_path: symbols we will use to write out new source code
    :param normalized_symbol: used to create a Symbol object
    :param is_symbol_of_interest: predicate that determines if a symbol is of interest
    :return: Symbol object
    """
    queue = collections.deque()
    root_symbol = symbol_creator.create(project_root_path, normalized_symbol)
    queue.appendleft(root_symbol)
    while queue:
        current = queue.pop()
        for nested_normalized_symbol in collect_nested_symbols(current.normalized_symbol):
            if is_symbol_of_interest(sys.modules[normalized_symbol.module], nested_normalized_symbol):
                nested_symbol_object = symbol_creator.create(project_root_path, nested_normalized_symbol)
                current.nested_symbols.append(nested_symbol_object)
                queue.appendleft(nested_symbol_object)
    return root_symbol

def collect(project_root_path, module, is_symbol_of_interest):
    """
    collect symbols of interest contained in a module
    :param project_root_path: symbols we will use to write out new source code
    :param module: used to collect symbols
    :param is_symbol_of_interest: predicate that determines if a symbol is of interest
    :return: set of symbols of interest
    """
    filtered_symbols = set()
    for normalized_symbol in collect_nested_symbols(NormalizedModuleSymbol(module)):
        if is_symbol_of_interest(module, normalized_symbol):
            filtered_symbols.add(convert_to_symbol_object(project_root_path, normalized_symbol, is_symbol_of_interest))
    return filtered_symbols
