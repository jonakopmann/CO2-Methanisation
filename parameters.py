import numpy as np


class Parameters:
    # start mole fractions
    w_h2_0 = 0.15
    w_co2_0 = 0.85
    w_ch4_0 = 0
    w_h2o_0 = 0
    w_ar = 1 - w_h2_0 - w_co2_0 - w_ch4_0 - w_h2o_0

    # stoichiometric factors
    v_h2 = -4
    v_co2 = -1
    v_ch4 = 1
    v_h2o = 2

    # diffusion volumes
    delta_v_h2 = 6.12  # [cm^3]
    delta_v_co2 = 26.7  # [cm^3]
    delta_v_ch4 = 25.14  # [cm^3] TODO: not found in perrys book
    delta_v_h2o = 13.1  # [cm^3]

    # molar masses
    M_co2 = 44.0095  # [g/mol]
    M_h2 = 2.01588  # [g/mol]
    M_ch4 = 16.0425  # [g/mol]
    M_h2o = 18.0153  # [g/mol]
    M_0 = (w_co2_0 / M_co2 + w_h2_0 / M_h2 + w_ch4_0 / M_ch4 + w_h2o_0 / M_h2o) ** -1  # [g/mol]

    # dynamic const
    delta_y = 0.05
    delta_T = 0
    f_y = 2  # [1/s]
    f_T = 0.5  # [1/s]

    # constants
    p_0 = 1  # [bar]
    c_p = 880 * 1e-3  # [J/(K*g)]
    roh_s = 2350 * 1e3  # [g/m^3]
    epsilon = 0.5
    tau = 3
    D_i_eff = 1  # [mm^2/s]
    lambda_eff = 0.67 * 1e-3  # [W/(mm*K)]
    n = 2
    R = 8.314463  # [J/(mol*K)]
    d_pore = 20e-9  # [m]

    # reference values
    T_ref = 555  # [K]
    k_0_ref = 3.46e-4  # [mol/(bar*s*g)]
    EA = 77.5 * 1e3  # [J/mol]
    K_oh_ref = 0.5  # [1/bar^0.5]
    delta_H_oh = 22.4 * 1e3  # [J/mol]
    K_h2_ref = 0.44  # [1/bar^0.5]
    delta_H_h2 = -6.2 * 1e3  # [J/mol]
    K_mix_ref = 0.88  # [1/bar^0.5]
    delta_H_mix = -10 * 1e3  # [J/mol]

    # integration params
    r_steps = 50
    r_max = 1.5  # [mm]
    h = r_max / r_steps  # [mm]
    T_0 = 555  # [K]
    t_steps = 100
    t_i = np.linspace(0, 1, t_steps)  # [s]
