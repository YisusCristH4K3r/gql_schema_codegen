from typing import NamedTuple, Optional

from ..base import BaseInfo
from ..constants.constants import VALUE_TYPES
from ..dependency.dependency import Dependency, DependencyGroup


class ScalarInfo(NamedTuple):
    name: str
    value: Optional[str]


class ScalarType(BaseInfo):
    def __init__(self, info: ScalarInfo, dependency_group: DependencyGroup) -> None:
        super().__init__(info)
        self.dependency_group = dependency_group

    @property
    def file_representation(self):
        if str(self.name) == "DateTime":
            self.dependency_group.add_dependency(
                Dependency(imported_from="dataclasses", dependency="dataclass")
            )
            self.dependency_group.add_dependency(
                Dependency(imported_from="dataclasses", dependency="field")
            )
            self.dependency_group.add_dependency(
                Dependency(imported_from="datetime", dependency="datetime")
            )
            self.dependency_group.add_direct_dependency("dateutil.parser")
            return f"{self.name} = datetime"

        if not isinstance(self.value, str):
            self.dependency_group.add_dependency(
                Dependency(imported_from="typing", dependency="Any")
            )

            return f"{self.name} = Any"

        if self.name == "Property":
            self.dependency_group.add_dependency(
                Dependency(imported_from="typing", dependency="Union")
            )
            self.dependency_group.add_dependency(
                Dependency(imported_from="datetime", dependency="datetime")
            )
            self.dependency_group.add_dependency(
                Dependency(imported_from="typing", dependency="List")
            )
            self.dependency_group.add_dependency(
                Dependency(imported_from="decimal", dependency="Decimal")
            )
            return f"{self.name} = {self.value}"

        if self.value in list(VALUE_TYPES.values()):
            return f"{self.name} = {self.value}"

        self.dependency_group.add_dependency(
            Dependency(imported_from="typing", dependency="ClassVar")
        )

        return f"{self.name} = ClassVar['{self.value}']"

    def __repr__(self) -> str:
        return self.file_representation
