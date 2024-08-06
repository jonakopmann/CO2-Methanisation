import array
import math
import os

import casadi as ca
import numpy as np

from context import Context
from diffusion import Diffusion
from diffusion_coefficient import DiffusionCoefficient
from heat_conduction import HeatConduction
from parameters import Parameters
from plotter import Plotter
from reaction import Reaction


class Integrator:
    def __init__(self, params: Parameters, debug=False):
        self.params = params
        self.diff = Diffusion(self.params)
        self.d_i_eff = DiffusionCoefficient(self.params)
        self.reaction = Reaction(self.params)
        self.heat_cond = HeatConduction(self.params)
        self.debug = debug

    def get_D_i_j(self, T, p, M_i, M_j, v_i, v_j):
        return 1e-1 * (T ** 1.75) * (((M_i ** -1) + (M_j ** -1)) ** 0.5) / (
                p * 0.98692327 * ((v_i ** (1 / 3)) + (v_j ** (1 / 3))) ** 2)

    def get_D_i_m(self, y_i, y_j_1, y_j_2, y_j_3, D_i_j_1, D_i_j_2, D_i_j_3):
        return (1 - y_i) / ((y_j_1 / D_i_j_1) + (y_j_2 / D_i_j_2) + (y_j_3 / D_i_j_3))

    def get_D_i_Kn(self, T, M_i):
        return self.params.d_pore / 3 * ca.sqrt(8e3 * self.params.R * T / (ca.pi * M_i))

    def run(self):
        slices = int(self.params.f_w * self.params.t_max)
        self.params.t_steps = int((self.params.t_steps + 1) / slices) * slices
        self.params.t_i = np.linspace(0, self.params.t_max, self.params.t_steps)
        step_size = self.params.t_steps / slices
        res_final = {'xf': [], 'zf': []}
        for k in range(slices):
            # create context
            ctx = Context(self.params)

            # create ode variables
            ode_co2 = ca.SX(self.params.r_steps, 1)
            ode_ch4 = ca.SX(self.params.r_steps, 1)
            ode_h2 = ca.SX(self.params.r_steps, 1)
            ode_T = ca.SX(self.params.r_steps, 1)
            alg_p = ca.SX(self.params.r_steps, 1)

            alg_D_co2 = ca.SX(self.params.r_steps, 1)
            alg_D_ch4 = ca.SX(self.params.r_steps, 1)
            alg_D_h2 = ca.SX(self.params.r_steps, 1)

            # create boundary conditions for the surface values
            alg_co2_surf = (ctx.w_co2_fl * ctx.roh_fl - (ctx.D_co2_eff[-1] / ctx.beta_co2
                            * (ctx.w_co2_surf * ctx.roh_surf - ctx.w_co2[-1] * ctx.roh[-1])
                            / self.params.h).printme(0) - ctx.w_co2_surf * ctx.roh_surf)
            alg_ch4_surf = (ctx.w_ch4_fl * ctx.roh_fl / self.params.M_ch4 - ctx.D_ch4_eff[-1] / ctx.beta_ch4
                            * (ctx.w_ch4_surf * ctx.roh_surf - ctx.w_ch4[-1] * ctx.roh[-1])
                            / self.params.h - ctx.w_ch4_surf * ctx.roh_surf)
            alg_h2_surf = (ctx.w_h2_fl * ctx.roh_fl - ctx.D_h2_eff[-1] / ctx.beta_h2
                           * (ctx.w_h2_surf * ctx.roh_surf - ctx.w_h2[-1] * ctx.roh[-1])
                           / self.params.h - ctx.w_h2_surf * ctx.roh_surf)
            alg_T_surf = (ctx.T_fl - (self.params.lambda_eff / ctx.alpha * (ctx.T_surf - ctx.T[-1]) / self.params.h)
                          - ctx.T_surf)

            # assign equations to ode for each radius i
            for i in range(self.params.r_steps):
                # get reaction rate
                r = self.reaction.get_r(ctx, i)

                # odes for w, T and p
                ode_co2[i] = (self.diff.get_term(ctx.w_co2, ctx.w_co2_surf, i, ctx.D_co2_eff[i])
                              + self.reaction.get_mass_term(self.params.M_co2, ctx.roh[i], self.params.v_co2, r))
                ode_ch4[i] = (self.diff.get_term(ctx.w_ch4, ctx.w_ch4_surf, i, ctx.D_ch4_eff[i])
                              + self.reaction.get_mass_term(self.params.M_ch4, ctx.roh[i], self.params.v_ch4, r))
                ode_h2[i] = (self.diff.get_term(ctx.w_h2, ctx.w_h2_surf, i, ctx.D_h2_eff[i])
                             + self.reaction.get_mass_term(self.params.M_h2, ctx.roh[i], self.params.v_h2, r))
                ode_T[i] = self.heat_cond.get_term(ctx, i) + self.reaction.get_heat_term(ctx.T[i], r)
                alg_p[i] = (self.params.M_0 * ctx.T[i]) / (ctx.M[i] * self.params.T_0) * self.params.p_0 - ctx.p[i]

                # init binary diffusion coefficients
                self.d_i_eff.init(ctx, i)

                # alg for D_i_eff
                alg_D_co2[i] = self.d_i_eff.get_D_co2(ctx, i) - ctx.D_co2_eff[i]
                alg_D_h2[i] = self.d_i_eff.get_D_h2(ctx, i) - ctx.D_h2_eff[i]
                alg_D_ch4[i] = self.d_i_eff.get_D_ch4(ctx, i) - ctx.D_ch4_eff[i]

            # make input dynamic
            if k & 1 == 0:
                alg_co2_fl = (self.params.w_co2_0 + self.params.delta_w - ctx.w_co2_fl)
                alg_h2_fl = (self.params.w_h2_0 - self.params.delta_w - ctx.w_h2_fl)
                alg_T_fl = self.params.T_0 + self.params.delta_T - ctx.T_fl
            else:
                alg_co2_fl = (self.params.w_co2_0 - self.params.delta_w - ctx.w_co2_fl)
                alg_h2_fl = (self.params.w_h2_0 + self.params.delta_w - ctx.w_h2_fl)
                alg_T_fl = self.params.T_0 - self.params.delta_T - ctx.T_fl
            alg_ch4_fl = (self.params.w_ch4_0 - ctx.w_ch4_fl)

            # create integrator
            dae = {
                'x': ca.veccat(ctx.w_co2, ctx.w_ch4, ctx.w_h2, ctx.T),
                'z': ca.vertcat(ctx.w_co2_surf, ctx.w_ch4_surf, ctx.w_h2_surf, ctx.T_surf,
                                ctx.w_co2_fl, ctx.w_ch4_fl, ctx.w_h2_fl, ctx.T_fl,
                                ctx.D_co2_eff, ctx.D_ch4_eff, ctx.D_h2_eff, ctx.p),
                't': ctx.t,
                'ode': ca.vertcat(ode_co2, ode_ch4, ode_h2, ode_T),
                'alg': ca.vertcat(alg_co2_surf, alg_ch4_surf, alg_h2_surf, alg_T_surf,
                                  alg_co2_fl, alg_ch4_fl, alg_h2_fl, alg_T_fl,
                                  alg_D_co2, alg_D_ch4, alg_D_h2, alg_p)
            }

            options = {'regularity_check': True}
            if self.debug:
                options['verbose'] = True
                options['monitor'] = 'daeF'

            integrator = ca.integrator('I', 'idas', dae, k * self.params.t_max / slices,
                                       self.params.t_i[int(k * step_size):int(k * step_size + step_size)], options)

            # create initial values
            if k == 0:
                w_co2_0 = np.full(self.params.r_steps, self.params.w_co2_0)
                w_ch4_0 = np.full(self.params.r_steps, self.params.w_ch4_0)
                w_h2_0 = np.full(self.params.r_steps, self.params.w_h2_0)
                T_0 = np.full(self.params.r_steps, self.params.T_0)
                x0 = ca.vertcat(w_co2_0, w_ch4_0, w_h2_0, T_0)

                z0 = ca.vertcat(self.params.w_co2_0, self.params.w_ch4_0, self.params.w_h2_0, self.params.T_0,
                                self.params.w_co2_0, self.params.w_ch4_0, self.params.w_h2_0, self.params.T_0,
                                np.full(self.params.r_steps, 1), np.full(self.params.r_steps, 1),
                                np.full(self.params.r_steps, 1), np.full(self.params.r_steps, 1))
            else:
                x0 = res_final['xf'][:, -1]
                z0 = res_final['zf'][:, -1]

            # integrate
            res = integrator(x0=x0, z0=z0)
            res_final['xf'] = ca.horzcat(res_final['xf'], res['xf'])
            res_final['zf'] = ca.horzcat(res_final['zf'], res['zf'])

        res_x = ca.vertsplit(res_final['xf'], self.params.r_steps)
        res_z = ca.vertsplit(res_final['zf'])

        # add surface values
        res_w_co2 = ca.vertcat(res_x[0], res_z[0])
        res_w_ch4 = ca.vertcat(res_x[1], res_z[1])
        res_w_h2 = ca.vertcat(res_x[2], res_z[2])
        res_w_h2o = 1 - res_w_co2 - res_w_ch4 - res_w_h2
        res_T = ca.vertcat(res_x[3], res_z[3])
        res_p = ca.vertcat(ca.vertcat(*res_z[-self.params.r_steps:]), res_z[-self.params.r_steps:][-1])
        res_err = 1 - res_w_co2.full() - res_w_h2.full() - res_w_ch4.full() - res_w_h2o.full()

        # print max error
        print(f'max error {np.max(res_err)}')

        # create plotter and plot
        plotter = Plotter(self.params.t_i, np.linspace(0, self.params.r_max, self.params.r_steps + 1),
                          res_w_co2.full(), res_w_h2.full(), res_w_ch4.full(), res_w_h2o.full(), res_T.full(),
                          res_p.full())

        path = f'plots_water/f-{self.params.f_w}_deltaw-{self.params.delta_w}_deltaT-{self.params.delta_T}_t-{self.params.t_max}'
        plotter.animate_w(os.path.join(path, 'weight.mp4'), 'Mass fractions over time', 1)
        plotter.animate_T(os.path.join(path, 'temp.mp4'), 'Temperature over time', 1, )
        # plotter.animate_Y(os.path.join(path, 'yield.mp4'), 'Yield over time', 1)
        # plotter.animate_y(os.path.join(path, 'mole.mp4'), 'Mole fractions over time', 1)
