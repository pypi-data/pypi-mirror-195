from enum import Enum


class AssaysGetAssayResultsResponse200ItemSummarizerType0Aggregation(str, Enum):
    EDGES = "Edges"
    DENSITY = "Density"
    CUMULATIVE = "Cumulative"

    def __str__(self) -> str:
        return str(self.value)
