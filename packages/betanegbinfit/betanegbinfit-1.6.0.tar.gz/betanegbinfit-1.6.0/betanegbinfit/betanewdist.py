# -*- coding: utf-8 -*-
import jax.numpy as jnp
from jax.lax import while_loop, fori_loop, cond, select, lgamma
from jax import jit, custom_jvp
from jax.scipy.special import logsumexp
# from .utils import frexp, logfrexp
import numpy as np

@custom_jvp
def frexp(x):
    x, power = jnp.frexp(x)
    return x, power

@frexp.defjvp
def frexp_jvp(primals, tangents):
  primals = frexp(primals[0])
  return primals, (tangents[0] * 2. ** -primals[1], 0.0)

@custom_jvp
def logfrexp(x):
    x /= jnp.log(2)
    power = jnp.round(x)
    x = x - power
    return x, power

@logfrexp.defjvp
def logfrexp_jvp(primals, tangents):
  primals = logfrexp(primals[0])
  return primals, (tangents[0], 0.0)

def _calc_frac(a, b, c, z, i):
    return ((a + i) / (i + 1)) * ((b + i) / (c + i)) * z

def hyp2f1(a, b, c, z, eps=1e-16, n_max=1000):
    def body(carry):
        last_pos_res, last_pos_exp, res, prev_res, term, exp, i = carry
        term *= _calc_frac(a, b, c, z, i)
        prev_res = res
        res, p = frexp(res + term)
        term /= 2 ** p
        exp += p
        last_pos_res, last_pos_exp = cond(res > 0, lambda: (res, exp), lambda: (last_pos_res, last_pos_exp))
        return last_pos_res, last_pos_exp, res, prev_res, term, exp, i + 1
    def iter_cond(carry):
        _, _, res, prev_res, _, _, i = carry
        return (jnp.abs((res - prev_res) / res) > eps) & (i < n_max)
    res, exp = while_loop(iter_cond, body, (1., 0., 1., 0., 1.0, 0., 0))[:2]
    return jnp.log(res) + exp * jnp.log(2) 

def _calc_b1(a, b1, b2):
    return (4.0 - 3.0 * a + b1 + b2)/(a - 1.0)

def _calc_b2(a, b1, b2):
    return (3. * a - 2. * b1 - 2.0 * b2 - 5.0) / (a - 1.) + b1 * b2/((a - 1.) * (a - 2.))

def _calc_b3(a, b1, b2):
    return -((a - b1 - 2.) / (a - 1.)) * ((a - b2 - 2.) / (a - 2.))

def _calc_c1(a, a2, a3):
    return (2. * a - a2 - a3 - 3.)/(a - 1.)

def _calc_c2(a, a2, a3):
    return (2. - a + a2 + a3) / (a - 1.) - a2 * a3/((a - 1.) * (a - 2.))

def _calc_backward(i, a2, a3, b1, b2, z, f1, f2, f3, log=False):
    B1 = _calc_b1(i, b1, b2)
    B2 = _calc_b2(i, b1, b2)
    B3 = _calc_b3(i, b1, b2)
    C1 = _calc_c1(i, a2, a3)
    C2 = _calc_c2(i, a2, a3)
    alpha_1 = (B1 + C1 * z)
    alpha_2 =  (B2 + C2 * z)
    alpha_3 = B3
    # alpha_1 = select(jnp.abs(alpha_1)  < 1e-12, 1e-12, alpha_1)
    # alpha_2 = select(jnp.abs(alpha_2)  < 1e-12, 1e-12, alpha_2)
    # alpha_3 = select(jnp.abs(alpha_3)  < 1e-12, 1e-12, alpha_3)
    if log:
        b = jnp.array([alpha_1, alpha_2, alpha_3]) / (z - 1.)
        return logsumexp(jnp.array([f1, f2, f3]), b=b, )
    return (alpha_1 * f1 + alpha_2 * f2  + alpha_3 * f3) / (z - 1.)
from jax.experimental.host_callback import call
from scipy.special import hyp2f1 as hp2

@jnp.vectorize
def logprob_recurrent(x, r, p, k):
    z = 1. - p
    a2 = k * p + 1.
    a3 = 1. - r
    b1 = 2.
    b2 = 2. - k * (1. - p)  - r
    nonhyp_term = jnp.log1p(-p) + jnp.log(p) + jnp.log(r) + lgamma(1 + k) + lgamma(r + k * (1 - p) - 1.)
    t, _ = logsumexp(jnp.array([lgamma(k) + lgamma(k * (1. - p) + r),
                                 lgamma(k * (1. - p)) + lgamma(k + r)]),
                      b=jnp.array([1., -1.]), return_sign=True)
    nonhyp_term -= t
    hyp_1 = hyp2f1(1. + k * p, 1. - r, 2. + k * (-1. + p) - r, 1. - p)
    hyp_0 = hyp2f1(k * p, -r, 1. + k * (-1. + p) - r, 1. - p)
    t = -jnp.expm1(hyp_0)
    b_term = jnp.log(jnp.abs(t))
    hyp_0 = select(jnp.isfinite(b_term), b_term, hyp_0)
    hyp_0 += jnp.log(jnp.abs(1. - r - k * (1. - p))) - jnp.log(k) - jnp.log1p(-p) - jnp.log(p) - jnp.log(r)
    hyp_2 = _calc_backward(3., a2, a3, b1, b2, z, hyp_1, hyp_0, 0.0, log=True)
    f1 = hyp_2 + nonhyp_term + jnp.log(p) * 2.
    f2 = hyp_1 + nonhyp_term + jnp.log(p)
    f3 = hyp_0 + nonhyp_term
    f3, exp = logfrexp(f3)
    t = exp * jnp.log(2.)
    f2 -= t
    f1 -= t
    f1 = jnp.exp(f1)
    f2 = jnp.exp(f2)
    f3 = jnp.exp(f3)
    def body(i, carry):
        f1, f2, f3, exp = carry
        f1, f2, f3 = _calc_backward(i + 1, a2, a3, b1, b2, z, f1 * p, f2 * p ** 2., f3 * p ** 3.), f1, f2
        t = (f2 - f3) + f2
        f1 = select(f1 > 0, f1, select(t > 0, t, 0.0))
        f1, texp = frexp(f1)
        exp += texp
        f2 /= 2. ** texp
        f3 /= 2. ** texp
        return f1, f2, f3, exp
    res = fori_loop(3, x + 1, body, (f1, f2, f3, exp))    
    return jnp.log(res[0]) + res[-1] * jnp.log(2)

from jax.config import config
from os import environ

config.update("jax_enable_x64", True)
config.update("jax_platform_name", "cpu")
# rt = 10.
# pt = 0.5
# kt = 20.
# p = 0.5
# k = 3.
# r = 10.
p = 1/6 #0.5
k = 200.
r = 200.
x = 400

z = 1. - p
a2 = k * p + 1.
a3 = 1. - r
b1 = 2.
b2 = 2. - k * (1. - p)  - r
xt = jnp.arange(0,x) + 1

B1 = _calc_b1(xt, b1, b2)
B2 = _calc_b2(xt, b1, b2)
B3 = _calc_b3(xt, b1, b2)
C1 = _calc_c1(xt, a2, a3)
C2 = _calc_c2(xt, a2, a3)
alpha_1 = (B1 + C1 * z) * p / (z - 1)
alpha_2 =  (B2 + C2 * z) * p ** 2 / (z - 1)
alpha_3 = B3 * p ** 3 / (z - 1)
nonhyp_term = jnp.log1p(-p) + jnp.log(p) + jnp.log(r) + lgamma(1 + k) + lgamma(r + k * (1 - p) - 1.)
t, _ = logsumexp(jnp.array([lgamma(k) + lgamma(k * (1. - p) + r),
                             lgamma(k * (1. - p)) + lgamma(k + r)]),
                  b=jnp.array([1., -1.]), return_sign=True)
nonhyp_term -= t
hyp_1 = hyp2f1(1. + k * p, 1. - r, 2. + k * (-1. + p) - r, 1. - p)
hyp_0 = hyp2f1(k * p, -r, 1. + k * (-1. + p) - r, 1. - p)
t = -jnp.expm1(hyp_0)
b_term = jnp.log(jnp.abs(t))
hyp_0 = select(jnp.isfinite(b_term), b_term, hyp_0)
hyp_0 += jnp.log(jnp.abs(1. - r - k * (1. - p))) - jnp.log(k) - jnp.log1p(-p) - jnp.log(p) - jnp.log(r)
hyp_2 = _calc_backward(3., a2, a3, b1, b2, z, hyp_1, hyp_0, 0.0, log=True)
f1 = hyp_2 + nonhyp_term + jnp.log(p) * 2.
f2 = hyp_1 + nonhyp_term + jnp.log(p)
f3 = hyp_0 + nonhyp_term
f1 = jnp.exp(f1)
f2 = jnp.exp(f2)
f3 = jnp.exp(f3)
def fill_diagonal(a, val):
  assert a.ndim >= 2
  i, j = jnp.diag_indices(min(a.shape[-2:]))
  return a.at[..., i, j].set(val)
A = (jnp.diag(-alpha_3[3:], -3) + jnp.diag(-alpha_2[2:], -2) + jnp.diag(-alpha_1[1:], -1)) 
A = A.at[:3, :].set(0.0)
A = fill_diagonal(A, 1)
At = A.copy()
A = A.T @ A
# A=jnp.append(A, jnp.ones((len(xt),1), dtype=float), axis=1)
# A=jnp.vstack((A, jnp.ones(A.shape[-1])))
A=jnp.append(A, jnp.zeros((len(xt),1), dtype=float), axis=1)
A=jnp.vstack((A, jnp.zeros(A.shape[-1])))
# A = A.at[-1, -2].set(1)
# A = A.at[-2, -1].set(1)
# # tA = np.array(A).copy()

# A = A.at[:, -1].set(1.0)
# A = A.at[-1, :].set(1.0)
# A = A.at[-1, -1].set(0.0)

A = A.at[-1, -1].set(1.0)
A = A.at[-2, :].set(0.0)
A = A.at[:, -2].set(0.0)
A = A.at[-2, -2].set(1.0)
A = A.at[1:-2, 1:-2].get()

A=jnp.append(A, jnp.ones((A.shape[0],1), dtype=float), axis=1)
A=jnp.vstack((A, jnp.ones(A.shape[-1])))
A = A.at[-1, -1].set(0.0)


# A = A.at[-1, -1].set(1.0)
# A = A.at[-2, :].set(1.0)
# A = A.at[-1, :].set(0.0)
# A = A.at[-1, -1].set(1.0)
b = jnp.zeros(len(xt) + 1, dtype=float)
b = b.at[:3].set([f3, f2, f1])
# b = b.at[-1].set(1.0)
b = b.at[1:-1].get()
b = b.at[-1].set(1.0)
# b = b.at[-1].set(1)
# b = At.T @ b
# b = jnp.append(b, jnp.zeros(1))
from jax.scipy.linalg import solve_triangular
# # x = solve_triangular(A, b, lower=True, unit_diagonal=True)

import matplotlib.pyplot as plt
# AL = np.linalg.cholesky(A)
# d = AL.diagonal().reshape(-1, 1)
# for i in range(len(d)):
#     AL[:, i] /= d[i,0]
    # b = b.at[i].set(d[i,0])
# b /= d.flatten()
# AL = d ** 0.5 @ AL @ d
# inv = np.linalg.inv(AL)
# x = np.linalg.inv(AL.T) @ np.linalg.inv(AL) @ b
b_ = b.copy()
# A += np.
xsol  = jnp.linalg.inv(A) @ b

# plt.plot(x2[:100])
rbad = jnp.exp(logprob_recurrent(xt, r, p, k))
# plt.plot(jnp.exp(logprob_recurrent(xt, r, p, k)))
# plt.plot(xa[:100])


import sympy as sp
from sympy.core.add import Add
N  = 5
# alpha = sp.IndexedBase('alpha')
alpha_ = sp.Function('alpha')
beta_ = sp.Function('beta')
gamma_ = sp.Function('gamma')
M = sp.eye(N)
for i in range(3, N):
    M[i, i - 1] = -alpha_(i + 1)
    M[i, i - 2] = -beta_(i + 1)
    if i > 3:
        M[i, i - 3] = -gamma_(i + 1)
M2 = M.T @ M
for i in range(N):
    M2[-1, i] = 0
    M2[i, -1] = 0
M2[-1, -1] = 1
M2e = M2.row_join(sp.Matrix([0] * N))
M2e = M2e.col_join(sp.Matrix([0] * (N + 1)).T)
M2e[-1, -1] = 1
def convert(M, level):
    m = sp.var('m')
    M = M[level, :]
    lt = list()
    n = min(level + 4, len(M))
    for i in range(level - 3, n):
        expr = M[i]
        if isinstance(expr, Add):
            res = 0
            for arg in expr.args:
                subres = 1
                for sub in arg.args:
                    t = type(sub)
                    if t in (alpha_, beta_, gamma_):
                        arg = sub.args[0]
                        subres *= t(m + (arg - level))
                    else:
                        subres *= sub
                res += subres
        else:
            res = 1
            for sub in expr.args:
                t = type(sub)
                if t in (alpha_, beta_, gamma_):
                    arg = sub.args[0]
                    res *= t(m + (arg - level))
                else:
                    res *= sub
        lt.append(res)        
    return sp.Matrix(lt)
# R = convert(M2e, 7)
a = sp.IndexedBase('a')
b = sp.IndexedBase('b')
c = sp.IndexedBase('c')
d = sp.IndexedBase('d')
e = sp.IndexedBase('e')
f = sp.IndexedBase('f')
g = sp.IndexedBase('g')
M2 = sp.eye(N)
for i in range(1, N-1):
    if i > 1:
        M2[i, i - 1] = b[i]
    if i > 2:
        M2[i, i - 2] = c[i]
    if i > 3:
        M2[i, i - 3] = d[i]
    if i < N - 1:
        M2[i, i + 1] = e[i]
    if i < N - 2:
        M2[i, i + 2] = f[i]
    if i < N - 3:
        M2[i, i + 3] = g[i]
# M2 = M2 + M2.T
for i in range(1, N-1):
    M2[i, i] = a[i]
M2[0,0] = 1
M2[-1, -1] = 1

import numpy as np

def calc_coeffs(i, a2, a3, b1, b2, z, p):
    i += 1
    B1 = _calc_b1(i, b1, b2)
    B2 = _calc_b2(i, b1, b2)
    B3 = _calc_b3(i, b1, b2)
    C1 = _calc_c1(i, a2, a3)
    C2 = _calc_c2(i, a2, a3)
    alpha = (B1 + C1 * z) * p / (z - 1)
    beta =  (B2 + C2 * z) * p ** 2 / (z - 1)
    gamma = B3 * p ** 3 / (z - 1)
    return alpha, beta, gamma


def calc_aefg(alpha_1, alpha_2, alpha_3, alpha_4,
              beta_1, beta_2, beta_3, beta_4,
              gamma_1, gamma_2, gamma_3, gamma_4):
    a = alpha_2 ** 2 + beta_3 ** 2 + gamma_4 ** 2 + 1
    e = -alpha_2 + alpha_3 * beta_3 + beta_4 * gamma_4
    f = alpha_4 * gamma_4 - beta_3
    g = -gamma_4
    return a, e, f, g

def calc_first_aefg(alpha_1, alpha_2, alpha_3, alpha_4,
                 beta_1, beta_2, beta_3, beta_4,
                 gamma_1, gamma_2, gamma_3, gamma_4):
    a = beta_3 ** 2 + gamma_4 ** 2 + 1
    e = alpha_3 * beta_3 + beta_4 * gamma_4
    f = alpha_4 * gamma_4 - beta_3
    g = -gamma_4
    return a, e, f, g
    
    

def calc_last_aefg(alpha_1, alpha_2, alpha_3, alpha_4,
                    beta_1, beta_2, beta_3, beta_4,
                    gamma_1, gamma_2, gamma_3, gamma_4, i, i_max, c):
    di = i_max - i
    alphas = jnp.array([alpha_1, alpha_2, alpha_3, alpha_4])
    betas = jnp.array([beta_1, beta_2, beta_3, beta_4])
    gammas = jnp.array([gamma_1, gamma_2, gamma_3, gamma_4])
    # print(4 - c, c)
    alphas = alphas.at[:4-c].set(alphas.at[c:].get()); alphas = alphas.at[4-c:].set(0.)
    betas = betas.at[:4-c].set(betas.at[c:].get()); betas = betas.at[4-c:].set(0.)
    gammas = gammas.at[:4-c].set(gammas.at[c:].get()); gammas = gammas.at[4-c:].set(0.)
    
    aefg = calc_aefg(*alphas, *betas, *gammas)
    return aefg[0], aefg[1] * (di >= 1), aefg[2] * (di >= 2), 0.0
    
    
    


# def calc_first()

x = A.shape[0]
# def solve(x, r, p, k):
z = 1. - p
a2 = k * p + 1.
a3 = 1. - r
b1 = 2.
b2 = 2. - k * (1. - p)  - r
aux = jnp.zeros((x, 5), dtype=float)
aux = aux.at[:, 0].set(1.0)

nonhyp_term = jnp.log1p(-p) + jnp.log(p) + jnp.log(r) + lgamma(1 + k) + lgamma(r + k * (1 - p) - 1.)
t, _ = logsumexp(jnp.array([lgamma(k) + lgamma(k * (1. - p) + r),
                              lgamma(k * (1. - p)) + lgamma(k + r)]),
                  b=jnp.array([1., -1.]), return_sign=True)
nonhyp_term -= t
hyp_1 = hyp2f1(1. + k * p, 1. - r, 2. + k * (-1. + p) - r, 1. - p)
hyp_0 = hyp2f1(k * p, -r, 1. + k * (-1. + p) - r, 1. - p)
t = -jnp.expm1(hyp_0)
b_term = jnp.log(jnp.abs(t))
hyp_0 = select(jnp.isfinite(b_term), b_term, hyp_0)
hyp_0 += jnp.log(jnp.abs(1. - r - k * (1. - p))) - jnp.log(k) - jnp.log1p(-p) - jnp.log(p) - jnp.log(r)
hyp_2 = _calc_backward(3., a2, a3, b1, b2, z, hyp_1, hyp_0, 0.0, log=True)
f2 = hyp_2 + nonhyp_term + jnp.log(p) * 2.
f2 = jnp.exp(f2)
f1 = hyp_1 + nonhyp_term + jnp.log(p)
f1 = jnp.exp(f1)

aux = aux.at[0, -1].set(f1)
aux = aux.at[1, -1].set(f2)

i = 1
(alpha_1, alpha_2, alpha_3, alpha_4), (beta_1, beta_2, beta_3, beta_4),\
    (gamma_1, gamma_2, gamma_3, gamma_4) = calc_coeffs(jnp.arange(i, i + 4), a2, a3, b1, b2, z, p)
aefg = calc_first_aefg(alpha_1, alpha_2, alpha_3, alpha_4,
                       beta_1, beta_2, beta_3, beta_4,
                       gamma_1, gamma_2, gamma_3, gamma_4)
# print(aefg)
# aefg = (*aefg[:-1], 0.0)
print(*aefg)
aefg_1 = aefg
aefg_2 = (0.0, 0.0, 0.0, 0.0)
aefg_3 = aefg_2
aux = aux.at[0, :-1].set(aefg)
aux = aux.at[0, -1].set(f1)
aux = aux.at[1, -1].set(f2)
# print(f2 - aefg[0])
# MX = np.zeros((aux.shape[0], aux.shape[0]))
# MX[0,:4] = np.array(aefg)[:A.shape[0]]
# B = np.zeros_like(A)
# B[0] = f1
# B[1] = f2
# print(f2, f1)
def get_hats(aux, aefg, aefg_1, aefg_2, aefg_3, i):
    a_n, e_n, f_n, g_n = aefg
    b_n = aefg_1[1]
    c_n = aefg_2[2]
    d_n = aefg_3[3]
    beta = aux.at[i - 1, -1].get()
    a_1_hat, e_1_hat, f_1_hat, g_1_hat, beta_1_hat = aux.at[i - 2].get()
    a_2_hat, e_2_hat, f_2_hat, g_2_hat, beta_2_hat = aux.at[i - 3].get()
    a_3_hat, e_3_hat, f_3_hat, g_3_hat, beta_3_hat = aux.at[i - 4].get()
    # print('----')
    # print('Before corr', c_n, b_n)
    # c_n, b_n = c_n - e_3_hat / a_3_hat * d_n, b_n - f_3_hat / a_3_hat * d_n - e_2_hat / a_2_hat * c_n
    c_n = c_n - e_3_hat / a_3_hat * d_n
    b_n = b_n - f_3_hat / a_3_hat * d_n - e_2_hat / a_2_hat * c_n
    # print('After corr', c_n, b_n)
    beta_hat = beta - beta_3_hat / a_3_hat * d_n - beta_2_hat / a_2_hat * c_n - beta_1_hat / a_1_hat * b_n
    # print(a_n, g_3_hat / a_3_hat * d_n , f_2_hat / a_2_hat * c_n , e_1_hat / a_1_hat * b_n)
    a_hat = a_n - g_3_hat / a_3_hat * d_n - f_2_hat / a_2_hat * c_n - e_1_hat / a_1_hat * b_n
    # if i == 2:
    #     print('----')
    #     print(a_n, b_n, e_1_hat, a_1_hat, a_n - e_1_hat / a_1_hat * b_n)
    e_hat = e_n - g_2_hat / a_2_hat * c_n - f_1_hat / a_1_hat * b_n
    # print('---')
    # print(f_n, g_1_hat, a_1_hat, b_n)
    f_hat = f_n - g_1_hat / a_1_hat * b_n
    g_hat = g_n
    # a = max(0, i - 1 - 3)
    # at = abs(i - 1 - 3) * (a == 0)
    # b = min(i - 1 + 4, MX.shape[0])
    # bt = (MX.shape[0] - i  + 4) * (b == MX.shape[0]) + 7 * (b != MX.shape[0])
    # t = [d_n, c_n, b_n, a_n, e_n, f_n, g_n]
    # t = [0, 0, 0, a_hat, e_hat, f_hat, g_hat]
    # MX[i - 1, a:b] = t[at:bt]
    # B[i - 1] = beta
    # print(i - 1, *t)
    return a_hat, e_hat, f_hat, g_hat, beta_hat
for i in range(2, x - 2):
    alpha_1, beta_1, gamma_1 = calc_coeffs(i + 3, a2, a3, b1, b2, z, p)
    alpha_1, alpha_2, alpha_3, alpha_4 = alpha_2, alpha_3, alpha_4, alpha_1
    beta_1, beta_2, beta_3, beta_4 = beta_2, beta_3, beta_4, beta_1
    gamma_1, gamma_2, gamma_3, gamma_4 = gamma_2, gamma_3, gamma_4, gamma_1
    aefg = calc_aefg(alpha_1, alpha_2, alpha_3, alpha_4,
                     beta_1, beta_2, beta_3, beta_4,
                     gamma_1, gamma_2, gamma_3, gamma_4)
    # print(i, *aefg)
    aux = aux.at[i - 1].set(get_hats(aux, aefg, aefg_1, aefg_2, aefg_3, i))
    aefg_1, aefg_2, aefg_3 = aefg, aefg_1, aefg_2
i += 1
# print('slow')
alpha_1, beta_1, gamma_1 = calc_coeffs(i + 3, a2, a3, b1, b2, z, p)
alpha_1, alpha_2, alpha_3, alpha_4 = alpha_2, alpha_3, alpha_4, alpha_1
beta_1, beta_2, beta_3, beta_4 = beta_2, beta_3, beta_4, beta_1
gamma_1, gamma_2, gamma_3, gamma_4 = gamma_2, gamma_3, gamma_4, gamma_1
c = 0
# i = 1
for i in range(i, x + 1):
    aefg = calc_last_aefg(alpha_1, alpha_2, alpha_3, alpha_4,
                          beta_1, beta_2, beta_3, beta_4,
                          gamma_1, gamma_2, gamma_3, gamma_4, i, x, c)
    call(lambda x: print(x, ':'), i)
    call(lambda x: print(*x), aefg)
    # print(i, *aefg)
    aux = aux.at[i - 1].set(get_hats(aux, aefg, aefg_1, aefg_2, aefg_3, i))
    # call(lambda x: print(*x), aux.at[i - 1].get())
    aefg_1, aefg_2, aefg_3 = aefg, aefg_1, aefg_2
    c += 1

# i += 1
# # if i < x:
# aefg = calc_aefg(alpha_2, alpha_3, alpha_4, 0.,
#                  beta_2, beta_3, beta_4, 0.,
#                  gamma_2, gamma_3, gamma_4, 0.)
# aefg = (aefg[0], aefg[1], 0.0, 0.0)
# aux = aux.at[i - 1].set(get_hats(aux, aefg, aefg_1, aefg_2, aefg_3, i))
# aefg_1, aefg_2, aefg_3 = aefg, aefg_1, aefg_2

# i += 1
# aefg = calc_aefg(alpha_3, alpha_4, 0., 0.,
#                  beta_3, beta_4, 0., 0.,
#                  gamma_3, gamma_4, 0., 0.)
# aefg = (aefg[0], 0.0, 0.0, 0.0)
# aux = aux.at[i - 1].set(get_hats(aux, aefg, aefg_1, aefg_2, aefg_3, i))
# aefg_1, aefg_2, aefg_3 = aefg, aefg_1, aefg_2


f1 = 0.0
f2 = 0.0
f3 = 0.0
for i in reversed(range(aux.shape[0])):
    m, a, b, c, beta = aux.at[i].get()
    f = (beta - a * f1 - b * f2 - c * f3) / m
    aux = aux.at[i, -1].set(f)
    f1, f2, f3 = f, f1, f2

aux = np.array(aux)
A = np.array(A)

plt.figure()
plt.plot(xsol)
# plt.plot(aux[:, -1])
# A2 = np.zeros_like(A)
# A2[0, 0] = 1.0
# for i in range(1, A2.shape[0] + 1):
#     for j in range(i, min(A2.shape[0], i + 5)):
#         A2[i, j] = aux[i - 1, j - i]

    
    



