from dataclasses import dataclass


@dataclass
class PVModule:
    Name: str
    BIPV: str
    Date: str
    T_NOCT: float
    A_c: float
    N_s: int
    I_sc_ref: float
    V_oc_ref: float
    I_mp_ref: float
    V_mp_ref: float
    alpha_sc: float
    beta_oc: float
    a_ref: float
    I_L_ref: float
    I_o_ref: float
    R_s: float
    R_sh_ref: float
    Adjust: float
    gamma_r: float
    Version: str
    PTC: float
    Technology: str
    EgRef: float
    dEgdT: float
    irrad_ref: float
    temp_ref: float
