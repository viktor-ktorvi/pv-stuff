from dataclasses import dataclass

import hydra
import numpy as np
import numpy.typing as npt
from matplotlib import pyplot as plt
from omegaconf import OmegaConf
from pvlib import pvsystem

from src import CONFIGS_PATH
from src.config.config import Config
from src.plot.utils import set_rcParams


@dataclass
class PVModule:
    irradiance: float
    temperature: float
    alpha_sc: float
    a_ref: float
    I_L_ref: float
    I_o_ref: float
    R_sh_ref: float
    R_s: float
    EgRef: float
    dEgdT: float
    iv_curve_method: str

    def __post_init__(self):
        self._update_iv_curve()

    def _update_iv_curve(self):
        IL, I0, Rs, Rsh, nNsVth = pvsystem.calcparams_desoto(
            self.irradiance,
            self.temperature,
            alpha_sc=self.alpha_sc,
            a_ref=self.a_ref,
            I_L_ref=self.I_L_ref,
            I_o_ref=self.I_o_ref,
            R_sh_ref=self.R_sh_ref,
            R_s=self.R_s,
            EgRef=self.EgRef,
            dEgdT=self.dEgdT,
        )

        self.iv_curve_params = {
            "photocurrent": IL,
            "saturation_current": I0,
            "resistance_series": Rs,
            "resistance_shunt": Rsh,
            "nNsVth": nNsVth,
            "method": self.iv_curve_method,
        }

    def update(self, irradiance: float | None = None, temperature: float | None = None):
        if irradiance is not None:
            self.irradiance = irradiance

        if temperature is not None:
            self.temperature = temperature

        ambient_changed = irradiance is not None or temperature is not None

        if ambient_changed:
            self._update_iv_curve()

    def get_current(self, voltage: float | npt.NDArray):
        return pvsystem.i_from_v(voltage=voltage, **self.iv_curve_params)

    @property
    def curve_info(self):
        return pvsystem.singlediode(**self.iv_curve_params)


@hydra.main(version_base=None, config_path=str(CONFIGS_PATH), config_name="default")
def main(cfg: Config):
    """
    PV curve.

    Parameters
    ----------
    cfg: DictConfig
        Config.

    Returns
    -------
    """
    set_rcParams(cfg)
    print(OmegaConf.to_yaml(cfg))

    irradiance = cfg.pv_module.irrad_ref
    temperature = cfg.pv_module.temp_ref

    pv_module = PVModule(
        irradiance,
        temperature,
        alpha_sc=cfg.pv_module.alpha_sc,
        a_ref=cfg.pv_module.a_ref,
        I_L_ref=cfg.pv_module.I_L_ref,
        I_o_ref=cfg.pv_module.I_o_ref,
        R_sh_ref=cfg.pv_module.R_sh_ref,
        R_s=cfg.pv_module.R_s,
        EgRef=cfg.pv_module.EgRef,
        dEgdT=cfg.pv_module.dEgdT,
        iv_curve_method=cfg.iv_curve_method,
    )

    voltage = np.linspace(0.0, pv_module.curve_info["v_oc"], 100)
    current = pv_module.get_current(voltage)
    power = voltage * current

    fig, axs = plt.subplots(2, 1, sharex=True)
    axs[0].plot(voltage, current)
    axs[0].set_ylabel("I [A]")

    axs[1].plot(voltage, power)
    axs[1].set_ylabel("P [W]")
    axs[1].set_xlabel("V [V]")

    pv_module.update(irradiance=600, temperature=75)

    voltage = np.linspace(0.0, pv_module.curve_info["v_oc"], 100)
    current = pv_module.get_current(voltage)
    power = voltage * current

    axs[0].plot(voltage, current)
    axs[1].plot(voltage, power)

    plt.show()


if __name__ == "__main__":
    main()
