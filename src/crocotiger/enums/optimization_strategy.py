from enum import Enum


class OptimizationStrategy(Enum):
    BALANCED = "weighted_average"
    BROAD = "f_beta"
    STRICT = "constrained"
