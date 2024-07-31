import casadi as ca


def w_to_y(w_i, M_i, M):
    return w_i * M / M_i


def get_cp_co2(T):
    R = 8.314463  # [J/(mol*K)]
    M_co2 = 44.0095  # [g/mol]
    A = 514.5073
    B = 3.4923
    C = -0.9306
    D = -6.0861
    E = 54.1586
    F = -97.5157
    G = 70.9687
    t = T / (A + T)
    return R / M_co2 * (B + (C - B) * (t ** 2) * (1 - A / (A + T) * (D + E * t + F * (t ** 2) + G * (t ** 3))))


def get_cp_h2(T):
    R = 8.314463  # [J/(mol*K)]
    M_h2 = 2.01588  # [g/mol]
    A = 392.8422
    B = 2.4906
    C = -3.6262
    D = -1.9624
    E = 35.6197
    F = -81.3691
    G = 62.6668
    t = T / (A + T)
    return R / M_h2 * (B + (C - B) * (t ** 2) * (1 - A / (A + T) * (D + E * t + F * (t ** 2) + G * (t ** 3))))


def get_cp_ch4(T):
    R = 8.314463  # [J/(mol*K)]
    M_ch4 = 16.0425  # [g/mol]
    A = 1530.8043
    B = 4.2038
    C = -16.6150
    D = -3.5668
    E = 43.0563
    F = -86.5507
    G = 65.5986
    t = T / (A + T)
    return R / M_ch4 * (B + (C - B) * (t ** 2) * (1 - A / (A + T) * (D + E * t + F * (t ** 2) + G * (t ** 3))))


def get_cp_h2o(T):
    R = 8.314463  # [J/(mol*K)]
    M_h2o = 18.0153  # [g/mol]
    A = 706.3032
    B = 5.1703
    C = -6.0865
    D = -6.6011
    E = 36.2723
    F = -63.0965
    G = 46.2085
    t = T / (A + T)
    return R / M_h2o * (B + (C - B) * (t ** 2) * (1 - A / (A + T) * (D + E * t + F * (t ** 2) + G * (t ** 3))))


def get_H_co2(T):
    t = T / 1000
    A = 24.99735
    B = 55.18696
    C = -33.69137
    D = 7.948387
    E = -0.136638
    F = -403.6075
    H = -393.5224
    return A * t + B * t ** 2 / 2 + C * t ** 3 / 3 + D * t ** 4 / 4 - E / t + F - H


def get_H_h2(T):
    t = T / 1000
    A = 33.066178
    B = -11.363417
    C = 11.432816
    D = -2.772874
    E = -0.158558
    F = -9.980797
    H = 0.0
    return A * t + B * t ** 2 / 2 + C * t ** 3 / 3 + D * t ** 4 / 4 - E / t + F - H


def get_H_ch4(T):
    t = T / 1000
    A = -0.703029
    B = 108.4773
    C = -42.52157
    D = 5.862788
    E = 0.678565
    F = -76.84376
    H = -74.87310
    return A * t + B * t ** 2 / 2 + C * t ** 3 / 3 + D * t ** 4 / 4 - E / t + F - H


def get_H_h2o(T):
    t = T / 1000
    A = 30.09200
    B = 6.832514
    C = 6.793435
    D = -2.534480
    E = 0.082139
    F = -250.8810
    H = -241.8264
    return A * t + B * t ** 2 / 2 + C * t ** 3 / 3 + D * t ** 4 / 4 - E / t + F - H


def get_S_h2(T):
    t = T / 1000
    A = 33.066178
    B = -11.363417
    C = 11.432816
    D = -2.772874
    E = -0.158558
    G = 172.707974
    return A * ca.log(t) + B * t + (C / 2) * t ** 2 + (D / 3) * t ** 3 - E / (2 * t ** 2) + G


def get_S_co2(T):
    t = T / 1000
    A = 24.99735
    B = 55.18696
    C = -33.69137
    D = 7.948387
    E = -0.136638
    G = 228.2431
    return A * ca.log(t) + B * t + (C / 2) * t ** 2 + (D / 3) * t ** 3 - E / (2 * t ** 2) + G


def get_S_ch4(T):
    t = T / 1000
    A = -0.703029
    B = 108.4773
    C = -42.5215
    D = 5.862788
    E = 0.678565
    G = 158.7163
    return A * ca.log(t) + B * t + (C / 2) * t ** 2 + (D / 3) * t ** 3 - E / (2 * t ** 2) + G


def get_S_h2o(T):
    t = T / 1000
    A = 30.09200
    B = 6.832514
    C = 6.793435
    D = -2.534480
    E = 0.082139
    G = 223.3967
    return A * ca.log(t) + B * t + (C / 2) * t ** 2 + (D / 3) * t ** 3 - E / (2 * t ** 2) + G


def get_ny_co2(T, p):
    M_co2 = 44.0095  # [g/mol]
    R = 8.314463  # [J/(mol*K)]

    A = -0.18024
    B = 0.65989
    C = -0.37108
    D = 0.01586
    E = -0.00300
    return (1e9 * (A * 1e-5 + B * 1e-7 * T + C * 1e-10 * T ** 2 + D * 1e-12 * T ** 3 + E * 1e-15 * T ** 4)
            / (p * 1e5 * M_co2 / (R * T)))  # [mm^2/s]


def get_ny_h2(T, p):
    M_h2 = 2.01588  # [g/mol]
    R = 8.314463  # [J/(mol*K)]

    A = 0.18024
    B = 0.27174
    C = -0.13395
    D = 0.00585
    E = -0.00104
    return (1e9 * (A * 1e-5 + B * 1e-7 * T + C * 1e-10 * T ** 2 + D * 1e-12 * T ** 3 + E * 1e-15 * T ** 4)
            / (p * 1e5 * M_h2 / (R * T)))  # [mm^2/s]


def get_ny_ch4(T, p):
    M_h2 = 16.0425  # [g/mol]
    R = 8.314463  # [J/(mol*K)]

    A = -0.07759
    B = 0.50484
    C = -0.43101
    D = 0.03118
    E = -0.00981
    return (1e9 * (A * 1e-5 + B * 1e-7 * T + C * 1e-10 * T ** 2 + D * 1e-12 * T ** 3 + E * 1e-15 * T ** 4)
            / (p * 1e5 * M_h2 / (R * T)))  # [mm^2/s]


def get_ny_h2o(T, p):
    M_h2 = 18.0153  # [g/mol]
    R = 8.314463  # [J/(mol*K)]

    A = 0.64966
    B = -0.15102
    C = 1.15935
    D = -0.10080
    E = 0.03100
    return (1e9 * (A * 1e-5 + B * 1e-7 * T + C * 1e-10 * T ** 2 + D * 1e-12 * T ** 3 + E * 1e-15 * T ** 4)
            / (p * 1e5 * M_h2 / (R * T)))  # [mm^2/s]


def get_lambda_co2(T):
    A = -3.882
    B = 0.05283
    C = 0.071460
    D = -0.070310
    E = 0.018090
    return 1e-3 * (A * 1e-3 + B * 1e-3 * T + C * 1e-6 * T ** 2 + D * 1e-9 * T ** 3 + E * 1e-12 * T ** 4)  # [W/mm*K]


def get_lambda_h2(T):
    A = 0.651
    B = 0.76730
    C = -0.687050
    D = 0.506510
    E = -0.138540
    return 1e-3 * (A * 1e-3 + B * 1e-3 * T + C * 1e-6 * T ** 2 + D * 1e-9 * T ** 3 + E * 1e-12 * T ** 4)  # [W/mm*K]


def get_lambda_ch4(T):
    A = 8.154
    B = 0.00811
    C = 0.351530
    D = -0.338650
    E = 0.140920
    return 1e-3 * (A * 1e-3 + B * 1e-3 * T + C * 1e-6 * T ** 2 + D * 1e-9 * T ** 3 + E * 1e-12 * T ** 4)  # [W/mm*K]


def get_lambda_h2o(T):
    A = 13.918
    B = -0.04699
    C = 0.258066
    D = -0.183149
    E = 0.055092
    return 1e-3 * (A * 1e-3 + B * 1e-3 * T + C * 1e-6 * T ** 2 + D * 1e-9 * T ** 3 + E * 1e-12 * T ** 4)  # [W/mm*K]
