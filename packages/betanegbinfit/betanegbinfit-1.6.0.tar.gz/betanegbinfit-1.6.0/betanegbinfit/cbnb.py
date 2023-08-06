# -*- coding: utf-8 -*-
import jax.numpy as jnp
from jax.lax import while_loop, fori_loop, cond, select, lgamma
from jax import jit, custom_jvp
from jax.scipy.special import logsumexp
from functools import partial
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
    return x * jnp.log(2), power

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
    if log:
        b = jnp.array([alpha_1, alpha_2, alpha_3]) / (z - 1.)
        return logsumexp(jnp.array([f1, f2, f3]), b=b, )
    return (alpha_1 * f1 + alpha_2 * f2  + alpha_3 * f3) / (z - 1.)

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

    alphas = alphas.at[:4-c].set(alphas.at[c:].get()); alphas = alphas.at[4-c:].set(0.)
    betas = betas.at[:4-c].set(betas.at[c:].get()); betas = betas.at[4-c:].set(0.)
    gammas = gammas.at[:4-c].set(gammas.at[c:].get()); gammas = gammas.at[4-c:].set(0.)
    
    aefg = calc_aefg(*alphas, *betas, *gammas)
    return aefg[0], aefg[1] * (di >= 1), aefg[2] * (di >= 2), 0.0
    
def get_hats(aux, aefg, aefg_1, aefg_2, aefg_3, accum, i):
    a_n, e_n, f_n, g_n = aefg
    b_n = aefg_1[1]
    c_n = aefg_2[2] 
    d_n = aefg_3[3]
    beta = aux.at[i - 1, -1].get()
    a_1_hat, e_1_hat, f_1_hat, g_1_hat, h_1_hat, beta_1_hat = aux.at[i - 2].get()
    a_2_hat, e_2_hat, f_2_hat, g_2_hat, h_2_hat, beta_2_hat = aux.at[i - 3].get()
    a_3_hat, e_3_hat, f_3_hat, g_3_hat, h_3_hat, beta_3_hat = aux.at[i - 4].get()
    c_n = c_n - e_3_hat / a_3_hat * d_n
    b_n = b_n - f_3_hat / a_3_hat * d_n - e_2_hat / a_2_hat * c_n
    beta_hat = beta - beta_3_hat / a_3_hat * d_n - beta_2_hat / a_2_hat * c_n - beta_1_hat / a_1_hat * b_n
    a_hat = a_n - g_3_hat / a_3_hat * d_n - f_2_hat / a_2_hat * c_n - e_1_hat / a_1_hat * b_n
    e_hat = e_n - g_2_hat / a_2_hat * c_n - f_1_hat / a_1_hat * b_n
    f_hat = f_n - g_1_hat / a_1_hat * b_n
    g_hat = g_n
    h_hat = 1. - h_3_hat / a_3_hat * d_n - h_2_hat / a_2_hat * c_n - h_1_hat / a_1_hat * b_n
    accum -= 1#TODO
    return (a_hat, e_hat, f_hat, g_hat, beta_hat, h_hat), accum
    


# @partial(jit, static_argnums=(4,))
# @partial(jnp.vectorize, signature='(),(),(),()->(n)', excluded=(4,))
def logprob_recurrent(r, p, k, upper, max_sz):
    ahead_comp = 0
    x = upper + ahead_comp
    z = 1. - p
    a2 = k * p + 1.
    a3 = 1. - r
    b1 = 2.
    b2 = 2. - k * (1. - p)  - r
    aux = jnp.zeros((max_sz + ahead_comp, 6), dtype=float)
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
    # f2, pow2 = logfrexp(f2)
    f2 = jnp.exp(f2)
    f1 = hyp_1 + nonhyp_term + jnp.log(p)
    # f1, pow1 = logfrexp(f1)
    f1 = jnp.exp(f1) 
    f0 = hyp_0 + nonhyp_term
    accum = -jnp.expm1(f0)
    f0 = jnp.exp(f0)
    # call(lambda x: print(*x), (f0, f1, f2))
    
    i = 1
    (alpha_1, alpha_2, alpha_3, alpha_4), (beta_1, beta_2, beta_3, beta_4),\
        (gamma_1, gamma_2, gamma_3, gamma_4) = calc_coeffs(jnp.arange(i, i + 4), a2, a3, b1, b2, z, p)
    aefg = calc_first_aefg(alpha_1, alpha_2, alpha_3, alpha_4,
                           beta_1, beta_2, beta_3, beta_4,
                           gamma_1, gamma_2, gamma_3, gamma_4)
    
    aefg_1 = aefg
    aefg_2 = (0.0, 0.0, 0.0, 0.0)
    aefg_3 = aefg_2
    aux = aux.at[0, :-1].set(aefg)
    # aux = aux.at[0, :-1].multiply(2 ** -pow1)
    aux = aux.at[0, -1].set(f1)
    aux = aux.at[1, -1].set(f2)
    def main_body(i, carry):
        aux, aefgs, (alphas, betas, gammas) = carry
        aefg_1, aefg_2, aefg_3 = aefgs
        alpha_1, alpha_2, alpha_3, alpha_4 = alphas
        beta_1, beta_2, beta_3, beta_4 = betas
        gamma_1, gamma_2, gamma_3, gamma_4 = gammas
        alpha_1, beta_1, gamma_1 = calc_coeffs(i + 3, a2, a3, b1, b2, z, p)
        alpha_1, alpha_2, alpha_3, alpha_4 = alpha_2, alpha_3, alpha_4, alpha_1
        beta_1, beta_2, beta_3, beta_4 = beta_2, beta_3, beta_4, beta_1
        gamma_1, gamma_2, gamma_3, gamma_4 = gamma_2, gamma_3, gamma_4, gamma_1
        aefg = calc_aefg(alpha_1, alpha_2, alpha_3, alpha_4,
                         beta_1, beta_2, beta_3, beta_4,
                         gamma_1, gamma_2, gamma_3, gamma_4)
        aux = aux.at[i - 1].set(get_hats(aux, aefg, aefg_1, aefg_2, aefg_3, i))
        # call(lambda x: print(*x), (i, *aux.at[i - 1].get()))
        aefg_1, aefg_2, aefg_3 = aefg, aefg_1, aefg_2
        aefgs = (aefg_1, aefg_2, aefg_3)
        alphas = (alpha_1, alpha_2, alpha_3, alpha_4)
        betas = (beta_1, beta_2, beta_3, beta_4)
        gammas = (gamma_1, gamma_2, gamma_3, gamma_4)
        return aux, aefgs, (alphas, betas, gammas)
    
    aefg_1, aefg_2, aefg_3 = aefg, aefg_1, aefg_2
    aefgs = (aefg_1, aefg_2, aefg_3)
    alphas = (alpha_1, alpha_2, alpha_3, alpha_4)
    betas = (beta_1, beta_2, beta_3, beta_4)
    gammas = (gamma_1, gamma_2, gamma_3, gamma_4)
    aux, aefgs, (alphas, betas, gammas) = fori_loop(2, x - 2, main_body, (aux, aefgs, (alphas, betas, gammas)))
    aefg_1, aefg_2, aefg_3 = aefgs
    alpha_1, alpha_2, alpha_3, alpha_4 = alphas
    beta_1, beta_2, beta_3, beta_4 = betas
    gamma_1, gamma_2, gamma_3, gamma_4 = gammas

    i = x - 2
    alpha_1, beta_1, gamma_1 = calc_coeffs(i + 3, a2, a3, b1, b2, z, p)
    
    alpha_1, alpha_2, alpha_3, alpha_4 = alpha_2, alpha_3, alpha_4, alpha_1
    beta_1, beta_2, beta_3, beta_4 = beta_2, beta_3, beta_4, beta_1
    gamma_1, gamma_2, gamma_3, gamma_4 = gamma_2, gamma_3, gamma_4, gamma_1
    
    a = x - 2
    for c in range(3):
        i = a + c
        aefg = calc_last_aefg(alpha_1, alpha_2, alpha_3, alpha_4,
                              beta_1, beta_2, beta_3, beta_4,
                              gamma_1, gamma_2, gamma_3, gamma_4, i, x, c)
        aux = aux.at[i - 1].set(get_hats(aux, aefg, aefg_1, aefg_2, aefg_3, i))
        # call(lambda x: print(*x), (i, *aux.at[i - 1].get()))
        aefg_1, aefg_2, aefg_3 = aefg, aefg_1, aefg_2
    # return aux
    # return jnp.append(jnp.array([f0]), aux.at[:max_sz, -1].get())
    def backward_body(i, carry):
        aux, f1, f2, f3 = carry
        i = -i
        m, a, b, c, beta = aux.at[i].get()
        f = (beta - a * f1 - b * f2 - c * f3) / m
        f0 = f
        # f, p = frexp(f)
        # mult += p
        # f1 /= 2 ** p
        # f2 /= 2 ** p
        aux = aux.at[i, -1].set(f)
        return aux, f, f1, f2
    aux = fori_loop(-x + 1, 1, backward_body, (aux, 0.0, 0.0, 0.0))[0]
    # return aux
    return jnp.append(jnp.array([f0]), aux.at[:max_sz, -1].get())

    

p = 0.5
k = 200.
r = 100.
x = 200

max_sz = 1 + x
config.update("jax_enable_x64", True)
res = logprob_recurrent(r, p, k, x, max_sz)[:x]
print(res.sum())
plt.plot(res)
# print(res)