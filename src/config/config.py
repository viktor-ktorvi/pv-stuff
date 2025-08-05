from dataclasses import dataclass, field

from src.config.plotting.plotting import Plotting
from src.config.pv_module.pv_module import PVModule


@dataclass
class Config:
    random_seed: int
    iv_curve_method: str
    pv_module: PVModule = field(default_factory=PVModule)
    plotting: Plotting = field(default_factory=Plotting)
