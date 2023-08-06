#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 20:18:33 2023

@author: georgy
"""
import jax.numpy as jnp
from jax.lax import while_loop, fori_loop
from jax import jit
from gmpy2 import mpfr
from collections.abc import Iterable
from functools import partial


def _calc_frac(a, b, c, z, i):
    return (a + i) * (b + i) / ((i + 1) * (c + i)) * z

@partial(jit, inline=True)
def frexp(x):
    power = jnp.round(jnp.log2(jnp.abs(x))) + 1
    x *= 2.0 ** -power
    return x, power


@jit
@jnp.vectorize
def logprob(x, n, p):
    z = -p
    params, pfaff = (1.0 + n, 1.0 - x, 2.0, z), jnp.log1p(-z) * (n - x)
    
    def sum_iter(carry):
        res, prev_res, mult, term, i = carry
        frac = _calc_frac(*params, i - 1)
        term *= frac
        prev_res = res
        res, exp = frexp(res + term)
        term /= 2.0 ** exp
        mult += exp
        return res, prev_res, mult, term, i + 1
    
    def cond_iter(carry):
        res, prev_res = carry[:2]
        return (prev_res != res)
    
    term = 1.0
    res = 1.0
    mult = jnp.log(n) + jnp.log1p(-p) * n + jnp.log(p) * (x + 1) - jnp.log1p(-(1 - p) ** n)
    carry = while_loop(cond_iter, sum_iter, (res, 0, 0, term, 1))
    return jnp.log(carry[0]) + mult + carry[2] * jnp.log(2) + pfaff


@jit
@jnp.vectorize
def cdf(x, r, p):
    q = 1 - p
    f2 = jnp.exp(jnp.log1p(-p) * r + jnp.log(-1 + (1 + p) ** r) - jnp.log1p(-q ** r))
    f1 = jnp.exp(jnp.log(1 - p) * r + jnp.log(p) * 2 + jnp.log1p(p) * (r - 1) + jnp.log(r) - jnp.log1p(-q ** r))
    res = (x == 0) * f2 + (x > 0) * (f1 + f2)
    def sum_iter(x, carry):
        res, f1, f2 = carry
        alpha = p * (2 * (x - 1) + p * (-1 + r + x))
        beta = -(x - 2) * p  ** 2
        denom = (1 + p) * x
        f = (alpha * f1 + beta * f2) / denom
        res += f
        f2 = f1
        f1 = f
        return (res, f1, f2)
    return fori_loop(2, x.astype(int) + 1, sum_iter, (res, f1, f2))[0]


def long_cdf(x, r, p, skip=-1, return_dict=False):
    r = mpfr(r)
    p = mpfr(p)
    if not isinstance(x, Iterable):
        x = [x]
    f2 = (1 - p) ** r * (-1 + (1 + p) ** r) / (1 - (1 - p) ** r)
    f1 = (1 - p) ** r * p ** 2 * (1 + p) ** (r - 1) * r / (1 - (1 - p) ** r)
    # print(float(f1), float(f2))
    max_x = max(x)
    res = dict()
    res[0] = f2 if skip < 0 else 0
    res[1] = f1 + f2 if skip < 1 else 0
    for xt in range(2, max_x + 1):   
        alpha = p * (2 * (xt - 1) + p * (-1 + r + xt))
        beta = -(xt - 2) * p  ** 2
        denom = (1 + p) * xt
        f = (alpha * f1 + beta * f2) / denom
        if xt > skip:
            res[xt] = res[xt - 1] + f
        else:
            res[xt] = 0
        f2 = f1
        f1 = f
    if return_dict:
        return res
    return list(map(res.get, x))
