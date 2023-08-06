import importlib

import pytest
from picidae import lazily_echo, expand_parameter_list_by_x

from pavo_cristatus.module_symbols.callable_symbol import CallableSymbol
from pavo_cristatus.module_symbols.class_symbol import ClassSymbol
from pavo_cristatus.project_loader import project_loader
from pavo_cristatus.python_file import PythonFile
from pavo_cristatus.tests.doubles.verifiers.module_verifier import ModuleVerifier
from pavo_cristatus.tests.doubles.module_fakes.annotated.module_fake_class_with_callables import ModuleFakeClassWithCallables
from pavo_cristatus.tests.doubles.module_fakes.annotated.module_fake_class_with_classes import ModuleFakeClassWithClasses
from pavo_cristatus.tests.doubles.module_fakes.annotated.module_fake_class_with_inherited_annotated_callables import \
    ModuleFakeClassWithInheritedAnnotatedCallables
from pavo_cristatus.tests.doubles.module_fakes.annotated.module_fake_class_with_nested_annotated_callables import \
    ModuleFakeClassWithNestedAnnotatedCallables
from pavo_cristatus.tests.doubles.module_fakes.annotated.module_fake_class_with_classes_with_nested_annotated_callables import \
    ModuleFakeClassWithClassesWithNestedAnnotatedCallables
from pavo_cristatus.tests.doubles.module_fakes.annotated import module_fake_with_classes, \
    module_fake_with_imported_symbols_of_interest, module_fake_with_symbols_of_interest_set_to_variables, \
    module_fake_with_callables


@pytest.fixture
def monkey_patcher(monkeypatch):
    def monkey_patch(import_module_stub, collect_python_files_under_project_root_stub):
        monkeypatch.setattr(importlib, importlib.import_module.__name__, import_module_stub)
        monkeypatch.setattr(project_loader,
                            project_loader.collect_python_files_under_project_root.__name__,
                            collect_python_files_under_project_root_stub)
    return monkey_patch

class TestProjectLoader:

    def test_project_loader_successfully_handles_empty_modules(self, monkey_patcher):
        project_loader_stub = expand_parameter_list_by_x(lazily_echo(ModuleFakeClassWithCallables), 1)
        monkey_patcher(project_loader_stub, lazily_echo(list()))

        project_symbols = project_loader.load_annotated_project(str(), [])

        assert len(project_symbols) == 0

    def test_project_loader_filters_non_annotated_classes(self, monkey_patcher):
        module_verifier = ModuleVerifier(ModuleFakeClassWithClasses)
        module_verifier.add_expected_symbol_of_interest(ModuleFakeClassWithClasses.SymbolOfInterest)
        module_verifier.add_expected_non_symbol_of_interest(ModuleFakeClassWithClasses.NonSymbolOfInterest)
        module_verifier.set_expected_symbols_of_interest_type(ClassSymbol)

        module_verifier.verify(project_loader, monkey_patcher)

    def test_project_loader_filters_non_annotated_callables(self, monkey_patcher):
        module_verifier = ModuleVerifier(ModuleFakeClassWithCallables)
        module_verifier.add_expected_symbol_of_interest(ModuleFakeClassWithCallables.symbol_of_interest)
        module_verifier.add_expected_non_symbol_of_interest(ModuleFakeClassWithCallables.non_symbol_of_interest)
        module_verifier.set_expected_symbols_of_interest_type(CallableSymbol)

        module_verifier.verify(project_loader, monkey_patcher)

    def test_project_loader_filters_out_inherited_symbols_of_interest(self, monkey_patcher):
        project_loader_stub = lazily_echo(ModuleFakeClassWithInheritedAnnotatedCallables)
        monkey_patcher(project_loader_stub, lazily_echo([PythonFile(str(), str())]))

        project_symbols = project_loader.load_annotated_project(str(), [])

        # this should be expected. If a base class defines a method, that method should get picked up when that base
        # class is picked up
        assert len(next(iter(project_symbols)).normalized_symbols) == 0

    def test_project_loader_detects_nested_functions_as_symbol_of_interest(self, monkey_patcher):
        module_verifier = ModuleVerifier(ModuleFakeClassWithNestedAnnotatedCallables)
        module_verifier.add_expected_symbol_of_interest(ModuleFakeClassWithNestedAnnotatedCallables.symbol_of_interest)
        module_verifier.add_expected_non_symbol_of_interest(ModuleFakeClassWithNestedAnnotatedCallables.non_symbol_of_interest)
        module_verifier.set_expected_symbols_of_interest_type(CallableSymbol)

        module_verifier.verify(project_loader, monkey_patcher)

    def test_project_loader_detects_nested_functions_in_method_as_symbol_of_interest(self, monkey_patcher):
        module_verifier = ModuleVerifier(ModuleFakeClassWithClassesWithNestedAnnotatedCallables)
        module_verifier.add_expected_symbol_of_interest(ModuleFakeClassWithClassesWithNestedAnnotatedCallables.SymbolOfInterest)
        module_verifier.add_expected_non_symbol_of_interest(ModuleFakeClassWithClassesWithNestedAnnotatedCallables.NonSymbolOfInterest)
        module_verifier.set_expected_symbols_of_interest_type(ClassSymbol)

        module_verifier.verify(project_loader, monkey_patcher)

    def test_module_with_symbol_interest_that_is_set_to_variable(self, monkey_patcher):
        module_verifier = ModuleVerifier(module_fake_with_symbols_of_interest_set_to_variables)
        module_verifier.add_expected_symbol_of_interest(
            module_fake_with_symbols_of_interest_set_to_variables.symbol_of_interest)
        module_verifier.set_expected_symbols_of_interest_type(CallableSymbol)

        module_verifier.verify(project_loader, monkey_patcher)

    def test_project_loader_with_module_with_callable(self, monkey_patcher):
        module_verifier = ModuleVerifier(module_fake_with_callables)
        module_verifier.add_expected_symbol_of_interest(module_fake_with_callables.symbol_of_interest)
        module_verifier.add_expected_non_symbol_of_interest(module_fake_with_callables.non_symbol_of_interest)
        module_verifier.set_expected_symbols_of_interest_type(CallableSymbol)

        module_verifier.verify(project_loader, monkey_patcher)

    def test_project_loader_with_module_with_class(self, monkey_patcher):
        module_verifier = ModuleVerifier(module_fake_with_classes)
        module_verifier.add_expected_symbol_of_interest(module_fake_with_classes.SymbolOfInterest)
        module_verifier.add_expected_non_symbol_of_interest(module_fake_with_classes.NonSymbolOfInterest)
        module_verifier.set_expected_symbols_of_interest_type(ClassSymbol)

        module_verifier.verify(project_loader, monkey_patcher)

    def test_project_loader_with_module_with_imported_symbol_of_interest(self, monkey_patcher):
        module_verifier = ModuleVerifier(module_fake_with_imported_symbols_of_interest)
        module_verifier.add_expected_symbol_of_interest(module_fake_with_imported_symbols_of_interest.symbol_of_interest)
        module_verifier.add_expected_non_symbol_of_interest(
            module_fake_with_imported_symbols_of_interest.SymbolOfInterest)
        module_verifier.set_expected_symbols_of_interest_type(CallableSymbol)

        module_verifier.verify(project_loader, monkey_patcher)

