import json
from dataclasses import dataclass
from typing import List, NamedTuple, Optional, Sequence, Type, TypeVar

from dql.node import _fields

T = TypeVar("T", bound="DatasetRecord")


@dataclass
class DatasetRecord:
    id: int
    name: str
    description: Optional[str]
    labels: Sequence[str]
    shadow: bool
    versions: Optional[List[int]]

    @classmethod
    def parse(
        cls: Type[T],
        id: int,  # pylint: disable=redefined-builtin
        name: str,
        description: Optional[str],
        labels: str,
        shadow: int,
        version: Optional[int],
    ) -> T:
        labels_lst: List[str] = json.loads(labels)
        versions = None
        if version:
            versions = [version]

        return cls(id, name, description, labels_lst, bool(shadow), versions)

    def merge_versions(self, other: "DatasetRecord") -> None:
        """Merge versions from another dataset"""
        if other.id != self.id:
            raise RuntimeError("Cannot merge versions of datasets with different ids")
        if not other.versions:
            # nothing to merge
            return
        if not self.versions:
            self.versions = []

        self.versions = list(set(self.versions + other.versions))

    def has_version(self, version: int) -> bool:
        if not self.versions:
            return False
        return version in self.versions

    def is_valid_next_version(self, version: int) -> bool:
        """
        Checks if a number can be a valid next latest version for dataset.
        The only rule is that it cannot be lower than current latest version
        """
        if self.latest_version and self.latest_version >= version:
            return False
        return True

    def remove_version(self, version: int) -> None:
        if not self.versions or not self.has_version(version):
            return

        self.versions.remove(version)

    @property
    def registered(self) -> bool:
        return not self.shadow

    @property
    def next_version(self) -> int:
        """Returns what should be next autoincrement version of dataset"""
        if self.shadow or not self.versions:
            return 1
        return max(self.versions) + 1

    @property
    def latest_version(self) -> Optional[int]:
        """Returns latest version of a dataset"""
        if self.shadow or not self.versions:
            return None
        return max(self.versions)

    @property
    def prev_version(self) -> Optional[int]:
        """Returns previous version of a dataset"""
        if self.shadow or not self.versions or len(self.versions) == 1:
            return None

        return sorted(self.versions)[-2]


fields = [f for f in _fields if f[0] != "valid"]
# TODO use DatasetRowSchema when dataset query refactoring is done (merged)
# https://github.com/iterative/dql/pull/258
DatasetRow = NamedTuple(  # type: ignore
    "DatasetRow",
    fields + [("source", str)],
)
