from enum import Enum


class V1TaskGetByWorkspaceResponse200TasksItemStatusType3(str, Enum):
    RESOURCECONTENTION = "ResourceContention"

    def __str__(self) -> str:
        return str(self.value)
