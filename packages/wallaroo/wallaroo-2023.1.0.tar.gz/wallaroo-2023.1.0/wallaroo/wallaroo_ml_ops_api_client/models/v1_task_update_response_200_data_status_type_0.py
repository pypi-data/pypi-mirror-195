from enum import Enum


class V1TaskUpdateResponse200DataStatusType0(str, Enum):
    CRASHLOOP = "CrashLoop"

    def __str__(self) -> str:
        return str(self.value)
