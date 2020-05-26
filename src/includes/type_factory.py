from abc import abstractmethod

import typing

from src.api.tm_types import TmType
from src.errors import InconsistentTypesError


class TypeBuilder:
    def __init__(self, type_to_build):
        self.type_to_build = type_to_build

    @abstractmethod
    def build(self, value):
        pass


class TmTypeBuilder(TypeBuilder):
    def __init__(self, type_to_build):
        super().__init__(type_to_build)

    def build(self, value):
        if not isinstance(value, dict):
            raise InconsistentTypesError(f'dict expected, given: {type(value).__name__}')
        return self.type_to_build(value)


class PrimitiveTypeBuilder(TypeBuilder):
    def __init__(self, type_to_build):
        super().__init__(type_to_build)

    def build(self, value):
        if not isinstance(value, self.type_to_build):
            raise InconsistentTypesError(f'expected: {self.type_to_build.__name__}, given: {type(value).__name__}')
        return self.type_to_build(value)


class AnyTypeObjectFactory:
    def __init__(self, type_to_build, value):
        self.type_to_build = type_to_build
        self.value = value
        self.builder = self._get_builder()

    def _get_builder(self):
        if issubclass(self.type_to_build, TmType):
            return TmTypeBuilder(self.type_to_build)
        return PrimitiveTypeBuilder(self.type_to_build)

    @abstractmethod
    def create(self):
        pass


class ListTypeObjectFactory(AnyTypeObjectFactory):
    def __init__(self, type_to_build, value):
        super().__init__(type_to_build, value)

    def create(self):
        if not isinstance(self.value, list):
            raise InconsistentTypesError(f'expected list, given: {type(self.value).__name__}')
        return [self.builder.build(item) for item in self.value]


class TypeObjectFactory(AnyTypeObjectFactory):
    def __init__(self, type_to_build, value):
        super().__init__(type_to_build, value)

    def create(self):
        return self.builder.build(self.value)


class ObjectFactory:
    def __init__(self, type_name, value):
        self._type_name = type_name
        self._value = value
        self._factory = self._get_factory()

    def _get_factory(self):
        type_in_list = typing.get_args(self._type_name)
        if len(type_in_list) == 1:
            return ListTypeObjectFactory(*type_in_list, self._value)
        return TypeObjectFactory(self._type_name, self._value)

    def create(self):
        return self._factory.create()

