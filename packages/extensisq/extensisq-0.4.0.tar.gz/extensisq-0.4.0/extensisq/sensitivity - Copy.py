import numpy as np
from scipy.integrate import solve_ivp
from scipy.linalg import block_diag
from warnings import warn
from extensisq import BS5
from extensisq.common import calculate_scale, norm
from collections import namedtuple


SensitivityOutput = namedtuple("SensitivityOutput", "sensf yf sol")
AdjointSensitivityOutputInt = namedtuple("SensitivityOutput",
                                         "sens G sol_y sol_bw")
AdjointSensitivityOutputEnd = namedtuple("SensitivityOutput",
                                         "sens gf sol_y sol_bw")
PeriodicOutput = namedtuple("PeriodicOutput", "y0 success residual nit sol")


def _test_functions(fun, t0, y0, ndim, args=None, Np=None):
    """test the functions and embed args.
    if np is an integer, the size of the last axis should be np
    """
    assert callable(fun), f"{fun.__name__} should be a function"
    n = y0.size

    # test args
    if args is not None:
        try:
            _ = [*(args)]
        except TypeError:
            raise TypeError("`args` should be a tuple")

        def _fun(t, y, fun=fun, args=args):
            return np.asarray(fun(t, y, *args))
    else:
        _fun = fun

    # test function call
    try:
        test_value = _fun(t0, y0)
    except Exception:
        raise AssertionError(
            f"the function {fun.__name__} should have signature " +
            "f(t, y, *args) where *args is optional")

    # test returned ndim
    if test_value.ndim != ndim:
        raise ValueError(f"{fun.__name__} should return a {ndim}D array")

    # test returned shape
    expected_shape = ndim * [n]
    if Np is not None:
        expected_shape[-1] = Np
    for s, s_ex in zip(test_value.shape, expected_shape):
        if s != s_ex:
            raise ValueError(f"the array returned by {fun.__name__} " +
                             f"should have shape {expected_shape}")

    # return function with embedded args (and B) (and p)
    return _fun


#   Main methods


def sens_ID(fun, t_span, y0, jac, dfdp, dy0dp, p, atol=1e-6, rtol=1e-3,
            method=BS5, dense_output=False, t_eval=None, use_approx_jac=False):
    """Calculate the sensitivity at the end of a an ODE solution to real
    parameters p.

    The method is called forward sensitivity analysis by [1]_ and internal
    differentiation by [2]_.

    The initial value problem is:
        dy = fun(t, y, p),    y(t0) = y0(p)

    And the result of interest is dy/dp at the endpoint (tf). The problem that
    is solved has size ny*(np+1).

    Parameters
    ----------
    fun : callable
        The function of the ODE that is solved with solve_ivp. The calling
        signature is fun(t, y, *p). It should return an array of length (ny,).
        (Same as for calling solve_ivp)
    t_span : 2-tuple of floats
        Interval of integration (t0, tf). The solver starts with t=t0 and
        integrates until it reaches t=tf. (Same as for calling solve_ivp)
    y0 : array_like, shape (ny,)
        Initial state. (Same as for calling solve_ivp)
    jac : callable
        function with signature jac(t, y, *p) that returns the Jacobian
        dfun/dy as an array of size (ny,ny). Unlike for solve_ivp, this is not
        optional and jac should be callable.
    dfdp : callable
        function with signature dfdp(t, y, *p) that returns dfun/dp as an
        array of size (ny,np).
    dy0dp : array_like, shape (ny,np)
        Derivative dy0/dp of the initial solution y0 to the parameter p.
    p : array_like, shape (np,)
        contains the values of the parameters.
    method : solver class or string
        The ODE solver that is used. Default: BS5
    atol : float, or sequence of length ny
        The absolute tolerance for solve_ivp. Default: 1e-6.
    rtol : float
        The relative tolerance for solve_ivp. Default: 1e-3.
    dense_output : bool
        Set this to True if you want the output sol to have a dense output.
        Default: False
    t_eval : array_like or None, optional
        array of output points. The last point in `t_eval` should equal
        t_span[-1]. Default: None
    use_approx_jac : bool
        Use an approximate jacobian for the combined problem. This is only
        relevant for implicit methods. This can save functions calls to
        determine the jacobian numerically, but convergence with an incomplete
        jacobian depende on the solver. Default: False

    Returns
    -------
    sensf : array, shape (ny, np)
        The sensitivity dy/dp at the endpoint.
    yf : array, shape (n, )
        The solution at the endpoint.
    sol : OdeSolution
        The solver output containing the combined problem (flattend).

    References
    ----------
    .. [1] R. Serban, A.C. Hindmarsh, "CVODES: An ODE Solver with Sensitivity
           Analysis Capabilities", 2003
    .. [2] E. Hairer, G. Wanner, S.P. Norsett, "Solving Ordinary Differential
           Equations I", Springer Berlin, Heidelberg, 1993,
           https://doi.org/10.1007/978-3-540-78862-1
    """
    y0 = np.asarray(y0)
    p = np.asarray(p)
    Ny = y0.size
    Np = p.size
    if y0.dtype != np.float:
        raise ValueError("`y0` should have dtype float")

    dy0dp = np.asarray(dy0dp)

    # test inputs
    assert y0.ndim == 1, \
        "`y0` should be a 1d array"
    assert dy0dp.ndim == 2, \
        "`dy0dp` should be a 2d array of size (ny, np)"
    assert (Ny, Np) == dy0dp.shape, \
        "`dy0dp` should be a array of size (ny, np)"
    t0, tf = t_span

    if t_eval is not None:
        assert t_eval[-1] == tf, \
            'if `t_eval` is used, the last point should be t_span[-1]'

    fun = _test_functions(fun, t0, y0, 1, args=p)
    dfdp = _test_functions(dfdp, t0, y0, 2, args=p, Np=Np)
    jac = _test_functions(jac, t0, y0, 2, args=p)

    # set tolerance
    assert isinstance(rtol, float), 'rtol should be a float'
    assert isinstance(atol, float) or len(atol) == Ny, \
        '`atol` should be a float or a sequence of floats of length Ny'
    total_atol = np.empty((Np+1)*Ny)
    total_atol[:Ny] = atol
    for i, _p in enumerate(p, start=1):
        factor = abs(_p)
        factor = factor or 1.
        total_atol[i*Ny:(i+1)*Ny] = atol/factor

    # function to integrate
    def total_fun(t, total_y, fun=fun, dfdy=jac, dfdp=dfdp, Ny=Ny, Np=Np):
        y = total_y[:Ny]
        s = total_y[Ny:].reshape(Ny, Np, order='F')
        dy = fun(t, y)
        ds = dfdy(t, y) @ s + dfdp(t, y)
        return np.concatenate([dy, ds.reshape(-1, order='F')])

    # solve the combined IVP
    s0 = dy0dp
    total_y0 = np.concatenate([y0, s0.reshape(-1, order='F')])
    if not use_approx_jac:
        if method not in ['BDF', 'Radau']:
            sol = solve_ivp(total_fun, t_span, total_y0,
                            atol=total_atol, rtol=rtol, method=method,
                            dense_output=dense_output, t_eval=t_eval)
        else:
            jac_sparsity = np.zeros(2*[Ny*(Np+1)])
            jac_sparsity[:, :Ny] = 1
            for i in range(Np):
                jac_sparsity[(i+1)*Ny:(i+2)*Ny, (i+1)*Ny:(i+2)*Ny] = 1

            sol = solve_ivp(total_fun, t_span, total_y0,
                            atol=total_atol, rtol=rtol, method=method,
                            dense_output=dense_output, t_eval=t_eval,
                            jac_sparsity=jac_sparsity)
    else:

        def total_jac(t, y, jac=jac, Ny=Ny):
            """approximate Jacobian"""
            _y = y[:Ny]
            _jac = jac(t, _y)
            D = (Np + 1)*[_jac]
            return block_diag(*D)

        sol = solve_ivp(total_fun, t_span, total_y0,
                        atol=total_atol, rtol=rtol, method=method,
                        dense_output=dense_output, t_eval=t_eval,
                        jac=total_jac)
    if not sol.success:
        raise RuntimeError("IVP solver not converged")

    # output
    yf = sol.y[:Ny, -1]
    sensf = sol.y[Ny:, -1].reshape(Ny, Np, order='F')
    return SensitivityOutput(sensf, yf, sol)


def sens_adjoint_end(fun, t_span, y0, jac, dfdp, dy0dp, p, g, dgdp, dgdy,
                     method=BS5, rtol=1e-3, atol=1e-6, atol_lambda=1e-6,
                     atol_quad=1e-6, sol_y=None):
    """sensitivity for a scalar at time tf using the adjoint method.

    Define a function involving time, the solution of the IVP and parameters
    p: g(t, y, p). `sens_adjoint_tf` calculates its sensitivity at the end of
    the integration interval: dg(tf)/dp.

    The solutions sol_y and sol_mu are returned to make sensitivity analysis of
    the same problem for different parameters more efficient. solving for
    another function g requires a new sol_mu, and only sol_y can be reused in
    that case.

    fun : function(t, y, p) that returns array size (n,)
    t_span : (t0, tf)
    y0 : array size (n,)
    jac : function(t, y, p) that returns array size (n, n)
    p : array size (np,)
    dfdp : None or function(t, y, p) that returns array size(n, np)
    dy0dp : array size(n, dp)
    dgdp : function(t, y, p) that returns array size (np,) (partial derivative)
    dgdy : function(t, y, p) that returns array size (n,)
    """
    # test inputs
    y0 = np.asarray(y0)
    Ny = y0.size
    if y0.ndim != 1:
        raise ValueError("`y0` should be a 1d array")
    if y0.dtype != np.float:
        raise ValueError("`y0` should have dtype float")

    p = np.asarray(p)
    Np = p.size
    if p.ndim != 1:
        raise ValueError("`p` should be a 1d array")
    if p.dtype != np.float:
        raise ValueError("`p` should have dtype float")

    dy0dp = np.asarray(dy0dp)
    if dy0dp.ndim != 2:
        raise ValueError("`dy0dp` should be a 2d array of size (ny, np)")
    _Ny, _Np = dy0dp.shape
    if _Ny != Ny or _Np != Np:
        raise ValueError("`dy0dp` should be a array of shape (ny, np)")

    t0, tf = t_span
    fun = _test_functions(fun, t0, y0, 1, args=p)
    dfdp = _test_functions(dfdp, t0, y0, 2, args=p, Np=Np)
    jac = _test_functions(jac, t0, y0, 2, args=p)
    dgdy = _test_functions(dgdy, t0, y0, 1, args=p)
    dgdp = _test_functions(dgdp, t0, y0, 1, args=p, Np=Np)
    g = _test_functions(g, t0, y0, 1, args=p, Np=1)

    # forward solve of y
    if sol_y is not None:
        if sol_y.sol is None:
            raise ValueError("sol_y should have a dense output")
    else:
        if method in ("LSODA", "BDF", "Radau"):
            # implicit method
            sol_y = solve_ivp(
                fun, t_span, y0, method=method, atol=atol, rtol=rtol,
                dense_output=True, jac=jac)
        else:
            # explicit method
            sol_y = solve_ivp(
                fun, t_span, y0, method=method, atol=atol, rtol=rtol,
                dense_output=True)
        if not sol_y.success:
            raise RuntimeError(
                "IVP solver not converged in forward solve of y")

    # backward solve of adjoint problem with mu and xi combined
    # xi is for the integral
    def fun_bw(t, total_y, y=sol_y.sol, jac=jac, dfdp=dfdp, Ny=Ny):
        _mu = total_y[:Ny]
        _y = y(t)
        _jac = jac(t, _y)
        _dfdp = dfdp(t, _y)
        dmu = -(_jac.T @ _mu)
        dxi = _dfdp.T @ _mu
        return np.concatenate([dmu, dxi])

    yf = sol_y.sol(tf)
    yf_bw = np.concatenate([dgdy(tf, yf), np.zeros(Np)])
    atol_bw = np.zeros(Ny + Np)
    atol_bw[:Ny] = atol_lambda
    atol_bw[Ny:] = atol_quad

    if method not in ('LSODA', 'BDF', 'Radau'):
        # explicit method
        sol_bw = solve_ivp(fun_bw, (tf, t0), yf_bw, method=method,
                           atol=atol_bw, rtol=rtol)
    else:
        # implicit method
        def jac_bw(t, _, y=sol_y.sol, jac=jac, dfdp=dfdp, Ny=Ny, Np=Np):
            _y = y(t)
            _jac = jac(t, _y)
            _dfdp = dfdp(t, _y)
            jac_bw = np.zeros((Ny + Np, Ny + Np))
            jac_bw[:Ny, :Ny] = -_jac.T
            jac_bw[Ny:-1, :Ny] = _dfdp.T
            return jac_bw

        sol_bw = solve_ivp(fun_bw, (tf, t0), yf_bw, method=method,
                           atol=atol_bw, rtol=rtol, jac=jac_bw)
    if not sol_bw.success:
        raise RuntimeError(
            "IVP solver not converged in backward solve of lambda")

    # final result
    mu0 = sol_bw.y[:Ny, -1]
    integral = -sol_bw.y[Ny:, -1]
    sens = dgdp(tf, yf) + mu0 @ dy0dp + integral
    return AdjointSensitivityOutputEnd(sens, g(tf, yf), sol_y, sol_bw)


def sens_adjoint_int(fun, t_span, y0, jac, dfdp, dy0dp, p, g, dgdp, dgdy,
                     method=BS5, rtol=1e-3, atol=1e-6, atol_lambda=1e-6,
                     atol_quad=1e-6, sol_y=None):
    """sensitivity for a scalar at time tf using the adjoint method.

    Define a function involving time, the solution of the IVP and parameters
    p: g(t, y, p). `sens_adjoint_tf` calculates its sensitivity at the end of
    the integration interval: dg(tf)/dp.

    The solutions sol_y and sol_mu are returned to make sensitivity analysis of
    the same problem for different parameters more efficient. solving for
    another function g requires a new sol_mu, and only sol_y can be reused in
    that case.

    fun : function(t, y, p) that returns array size (ny,)
    t_span : (t0, tf)
    y0 : array size (n,)
    jac : function(t, y, p) that returns array size (n, n)
    p : array size (np,)
    dfdp : None or function(t, y, p) that returns array size(n, np)
    dy0dp : array size(n, dp)
    dgdp : function(t, y, p) that returns array size (np,) (partial derivative)
    dgdy : function(t, y, p) that returns array size (n,)
    """
    # test inputs
    y0 = np.asarray(y0)
    Ny = y0.size
    if y0.ndim != 1:
        raise ValueError("`y0` should be a 1d array")
    if y0.dtype != np.float:
        raise ValueError("`y0` should have dtype float")

    p = np.asarray(p)
    Np = p.size
    if p.ndim != 1:
        raise ValueError("`p` should be a 1d array")
    if p.dtype != np.float:
        raise ValueError("`p` should have dtype float")

    dy0dp = np.asarray(dy0dp)
    if dy0dp.ndim != 2:
        raise ValueError("`dy0dp` should be a 2d array of size (ny, np)")
    _Ny, _Np = dy0dp.shape
    if _Ny != Ny or _Np != Np:
        raise ValueError("`dy0dp` should be a array of shape (ny, np)")

    t0, tf = t_span
    fun = _test_functions(fun, t0, y0, 1, args=p)
    dfdp = _test_functions(dfdp, t0, y0, 2, args=p, Np=Np)
    jac = _test_functions(jac, t0, y0, 2, args=p)
    dgdy = _test_functions(dgdy, t0, y0, 1, args=p)
    dgdp = _test_functions(dgdp, t0, y0, 1, args=p, Np=Np)
    g = _test_functions(g, t0, y0, 1, args=p, Np=1)

    # forward solve of y
    if sol_y is not None:
        if sol_y.sol is None:
            raise ValueError("sol_y should have a dense output")
    else:
        if method in ("LSODA", "BDF", "Radau"):
            # implicit method
            sol_y = solve_ivp(
                fun, t_span, y0, method=method, atol=atol, rtol=rtol,
                dense_output=True, jac=jac)
        else:
            # explicit method
            sol_y = solve_ivp(
                fun, t_span, y0, method=method, atol=atol, rtol=rtol,
                dense_output=True)
        if not sol_y.success:
            raise RuntimeError(
                "IVP solver not converged in forward solve of y")

    # backward solve of adjoint problem with lambda, xi and zeta combined
    # xi is for the integral, zeta is for G
    def fun_bw(t, total_y, y=sol_y.sol, jac=jac, dgdy=dgdy, dgdp=dgdp,
               dfdp=dfdp, g=g, Ny=Ny):
        _lambda = total_y[:Ny]
        _y = y(t)
        _jac = jac(t, _y)
        _dgdy = dgdy(t, _y)
        _dgdp = dgdp(t, _y)
        _dfdp = dfdp(t, _y)
        dlambda = -(_jac.T @ _lambda + _dgdy.T)
        dxi = _dfdp.T @ _lambda + _dgdp
        dzeta = g(t, _y)
        return np.concatenate([dlambda, dxi, dzeta])

    yf_bw = np.zeros(Ny + Np + 1)
    atol_bw = np.zeros(Ny + Np + 1)
    atol_bw[:Ny] = atol_lambda
    atol_bw[Ny:] = atol_quad

    if method not in ('LSODA', 'BDF', 'Radau'):
        # explicit method
        sol_bw = solve_ivp(fun_bw, (tf, t0), yf_bw, method=method,
                           atol=atol_bw, rtol=rtol)
    else:
        # implicit method
        def jac_bw(t, _, y=sol_y.sol, jac=jac, dfdp=dfdp, Ny=Ny, Np=Np):
            _y = y(t)
            _jac = jac(t, _y)
            _dfdp = dfdp(t, _y)
            jac_bw = np.zeros((Ny + Np + 1, Ny + Np + 1))
            jac_bw[:Ny, :Ny] = -_jac.T
            jac_bw[Ny:-1, :Ny] = _dfdp.T
            return jac_bw

        sol_bw = solve_ivp(fun_bw, (tf, t0), yf_bw, method=method,
                           atol=atol_bw, rtol=rtol, jac=jac_bw)
    if not sol_bw.success:
        raise RuntimeError(
            "IVP solver not converged in backward solve of lambda")

    # final result
    lambda0 = sol_bw.y[:Ny, -1]
    integral = -sol_bw.y[Ny:-1, -1]
    G = -sol_bw.y[-1, -1]
    sens = lambda0 @ dy0dp + integral
    return AdjointSensitivityOutputInt(sens, G, sol_y, sol_bw)


#   Special purpose methods


def _sens_adjoint_y0(fun, t_span, y0, jac, method=BS5, **options):

    # forward solve of y
    options.pop('dense_output', None)
    sol_y = solve_ivp(fun, t_span, y0,
                      method=method, dense_output=True, **options)
    if not sol_y.success:
        raise RuntimeError("IVP solver not converged in forward solve of y")
    yf = sol_y.y[:, -1]

    # find the sensitivities
    #   g = y
    # solve per component of g (or y)
    options.pop('t_eval', None)
    t0, tf = t_span
    sens = []
    In = np.eye(len(y0))
    for _dgdy in In:

        # define derivative function of mu
        def fun_mu(t, mu, y=sol_y.sol, jac=jac):
            _y = y(t)
            _jac = jac(t, _y)
            return _jac.T @ -mu

        # backward solve of mu
        muf = _dgdy
        sol_mu = solve_ivp(fun_mu, (tf, t0), muf,
                           t_eval=[t0], method=method, **options)
        if not sol_mu.success:
            raise RuntimeError(
                "IVP solver not converged in backward solve of mu")

        mu0 = sol_mu.y[:, -1]
        sens.append(mu0)                                           # s(t0) = In
    sens = np.array(sens)
    return SensitivityOutput(sens, yf, sol_y)


def _sens_ID_y0(fun, t_span, y0, jac, method=BS5, hess=None, **options):
    """Calculate the sensitivity at the end of a an ODE solution to all initial
    values. The internal differentiation method is used. [1]_

    If the size of the original problem is n, the size of the problem that is
    solved to find the sensitivity to all initial values is n*(n+1).

    See also `extensisq.sensitivity` to calculate the sensitivity to a general
    (scalar) parameter.

    Parameters
    ----------
    fun : callable
        The function of the ODE that is solved with solve_ivp. The calling
        signature is fun(t, y). (Same as for calling solve_ivp)
    t_span : 2-tuple of floats
        Interval of integration (t0, tf). The solver starts with t=t0 and
        integrates until it reaches t=tf. (Same as for calling solve_ivp)
    y0 : array_like, shape (n, )
        Initial state. (Same as for calling solve_ivp)
    jac : callable
        function with signature jac(t, y) that returns the Jacobian dfun/dy
        as an n by n array. Unlike for solve_ivp, this is not optional and jac
        cannot be a matrix.
    method : solver class or {"RK45", "RK23", "DOP853"}
        The ODE solver that is used. This should be an explicit solver.
        Default: extensisq.BS5
    **options
        Options passed to solve_ivp. Options passed to solve_ivp. The option
        `vectorized` is ignored.

    Returns
    -------
    sens : array, shape (n, n)
        The sensitivity dy/dy0 at the endpoint is returned as an array of size
        n by n. The elements (i,j) are dy[i]/dy0[j].
    yf : array, shape (n, )
        The solution at the endpoint
    sol : OdeSolution
        The solver output containing the integrated problem and the
        sensitivities (flattend). Only returned if `full_output` is True.

    References
    ----------
    .. [1] E. Hairer, G. Wanner, S.P. Norsett, "Solving Ordinary Differential
           Equations I", Springer Berlin, Heidelberg, 1993,
           https://doi.org/10.1007/978-3-540-78862-1
    """
    N = y0.size

    # function to integrate
    def total_fun(t, total_y, fun=fun, dfdy=jac, N=N):
        y = total_y[:N]
        Psi = total_y[N:].reshape(N, N, order='F')
        dy = fun(t, y)
        dPsi = dfdy(t, y) @ Psi
        return np.concatenate([dy, dPsi.reshape(-1, order='F')])

    # corresponding Jacobian
    if hess is not None:

        def total_jac(t, y, jac=jac, hess=hess, N=N):
            _y = y[:N]
            _Psi = y[N:].reshape(N, N, order='F')
            _jac = jac(t, _y)
            _hess = hess(t, _y)
            D = (N+1)*[_jac]
            _total_jac = block_diag(*D)
            _L = (_hess @ _Psi).swapaxes(1, 2).reshape(N*N, N, order='F')
            _total_jac[N:, :N] = _L
            return _total_jac

    psi0 = np.eye(N, order='F')
    total_y0 = np.concatenate([y0, psi0.reshape(-1, order='F')])
    if hess is None:
        sol = solve_ivp(total_fun, t_span, total_y0, method=method,
                        **options)
    else:
        sol = solve_ivp(total_fun, t_span, total_y0, method=method,
                        jac=total_jac, **options)
    assert sol.success, f"IVP solver not converged; {sol.message}"

    # output sollution and sensitivity at end of integration
    sens = sol.y[N:, -1].reshape(N, N, order='F')
    yf = sol.y[:N, -1]
    return SensitivityOutput(sens, yf, sol)


def sens_y0(fun, t_span, y0, jac, sens_method='adjoint', hess=None,
            **options):
    """
    Calculate the sensitivity at the end of a an ODE solution to all initial
    values. The internal differentiation method is used. [1]_

    If the size of the original problem is n, the size of the problem that is
    solved to find the sensitivity to all initial values is n*(n+1).

    See also `extensisq.sensitivity` to calculate the sensitivity to a general
    (scalar) parameter.

    Parameters
    ----------
    fun : callable
        The function of the ODE that is solved with solve_ivp. The calling
        signature is fun(t, y). (Same as for calling solve_ivp)
    t_span : 2-tuple of floats
        Interval of integration (t0, tf). The solver starts with t=t0 and
        integrates until it reaches t=tf. (Same as for calling solve_ivp)
    y0 : array_like, shape (n, )
        Initial state. (Same as for calling solve_ivp)
    jac : callable
        function with signature jac(t, y) that returns the Jacobian dfun/dy
        as an n by n array. Unlike for solve_ivp, this is not optional and jac
        cannot be a matrix.
    sens_method : string {"adjoint", "ID"}
        The method that is used to calculate the sensisitivities: adjoint or
        internal integration (ID). Default: "adjoint"
    hess : callable
        function with signature jac(t, y) that returns the Jacobian ddfun/dy/dy
        as an n by n by n array. This is unly useful if both sens_method="ID"
        and an implicit integration method is used (like "BDF")
    **options
        Options passed to solve_ivp, like method (defaul BS5), atol, rtol. The
        option `vectorized` is ignored.

    Returns
    -------
    named tuple with 3 fields:
        sens : array, shape (n, n)
            The sensitivity dy/dy0 at the endpoint is returned as an array of
            size n by n. The elements (i,j) are dy[i]/dy0[j].
        yf : array, shape (n, )
            The solution at the endpoint
        sol : OdeSolution
            The solver output containing the integrated problem and the
            sensitivities (flattend). Only returned if `full_output` is True.

    References
    ----------
    .. [1] E. Hairer, G. Wanner, S.P. Norsett, "Solving Ordinary Differential
           Equations I", Springer Berlin, Heidelberg, 1993,
           https://doi.org/10.1007/978-3-540-78862-1
    .. [2] Adjoint method...
    """
    y0 = np.asarray(y0)

    options = options.copy()
    if options.pop("vectorized", False):
        warn("Vectorization is not supported and is switched off")

    # test inputs
    assert y0.ndim == 1, "`y0` should be a 1d array"
    t0 = t_span[0]
    options = options.copy()
    if options.pop("vectorized", False):
        warn("Vectorization is not supported and is switched off")

    args = options.pop("args", [])
    fun = _test_functions(fun, t0, y0, 1, args=args)
    jac = _test_functions(jac, t0, y0, 2, args=args)

    if sens_method == 'adjoint':
        return _sens_adjoint_y0(fun, t_span, y0, jac, **options)
    elif sens_method == 'ID':
        if hess is not None:
            hess = _test_functions(hess, t0, y0, 3, args=args)
        return _sens_ID_y0(fun, t_span, y0, jac, hess=hess, **options)
    else:
        raise ValueError("`sens_method` should be 'adjoint' or 'ID'")


def find_periodic_solution(fun, t_span, y0, jac, atol=1e-6, rtol=1e-3,
                           hess=None, max_iterations=8, **options):
    """Find a periodic solution of the problem, by tuning the initial
    conditions.

    A periodically forced (non-linear) solution may have a periodic solution
    for some specific initial values `y0` that are not known yet. This function
    tries to find this `y0` by running Newton Raphson iteration. The Jacobian
    for it is calculated using function `sensitivity_y0`.

    The period is defined by `t_span` and a resonably good initial estimate of
    `y0` is needed.

    Integrating again with the found y0 can result in a higher residual.
    Integration without using sensitivity_y0 results in different solver step
    sizes, which explains the difference. The tolerances can be set stricter to
    mitigate this.

    Parameters
    ----------
    fun : callable
        The function of the ODE that is solved with solve_ivp. The calling
        signature is fun(t, y). (Same as for calling solve_ivp)
    t_span : 2-tuple of floats
        Interval of integration (t0, tf). The solver starts with t=t0 and
        integrates until it reaches t=tf. The period of the integration tf - t0
        should be exactly one period.
    y0 : array_like, shape (n, )
        Initial state. This should be an approximation of the initial state of
        the periodic solution. The method may fail to converge if this estimate
        is poor.
    jac : callable
        Function with signature jac(t, y) that returns the Jacobian dfun/dy
        as an n by n array. Unlike for solve_ivp, this is not optional and jac
        cannot be a matrix.
    method : solver class or {"RK45", "RK23", "DOP853"}
        The ODE solver that is used. This should be an explicit solver.
        Default: extensisq.BS5
    atol : float, optional
        Absolute tolerance passed to `solve_ivp` and used for the stopping
        criteria of the Newton Raphson iteration. Default value: 1e-6
    rtol : float, optional
        Relative tolerance passed to `solve_ivp` and used for the stopping
        criteria of the Newton Raphson iteration. Default value: 1e-3
    max_iterations : int, optional
        Maximum number of correction to the initial value, by default 8.
    **options
        Options passed to solve_ivp. Options passed to solve_ivp. The option
        `vectorized` is ignored.

    Returns
    -------
    Object with results
        This object contains the OdeSolution entries of the last solve_ivp call
        (from `sensitivity_y0`, including the sensitivity solution), and some
        information from the Newton Raphson iteration:
            opt_success : bool
                True if the Newton Raphson iteration has converged. (Note: Do
                not confuse this with `success` from solve_ivp, which is also
                included in this object.
            opt_y0 : array_like, shape (n, )
                The found initial value for the periodic solution. The value
                from the last iteration is returned no matter the value of
                opt_succes.
            opt_residual : array_like, shape (n, )
                The remaining residual yf - y0.
            opt_nit : int
                The number of Newton Raphson iterations. The number of calls to
                `sensitivity_y0` is opt_nit + 1.
    """
    options["atol"] = atol
    options["rtol"] = rtol
    y0 = np.asarray(y0)
    N = y0.size
    In = np.eye(N) # , order='F' ?

    # Newton Raphson iteration
    correction_norm_old = None
    rate = np.inf
    for it in range(max_iterations+1):
        # calculate solution and sensitivity
        S0, yf, sol = _sens_ID_y0(fun, t_span, y0, jac, hess=hess, **options)
        residual = yf - y0
        jacobian = S0 - In
        correction = np.linalg.solve(jacobian, residual)
        scale = calculate_scale(atol, rtol, y0, yf)

        # assess solution
        correction_norm = norm(correction/scale)
        if correction_norm_old is not None:
            rate = correction_norm/correction_norm_old
        converged_solution = correction_norm < (1. - rate)

        # assess residual
        residual_norm = norm(residual/scale)
        converged_residual = residual_norm < 1.

        if converged_residual and converged_solution:
            # solution converged
            success = True
            break

        # update
        y0 -= correction
        correction_norm_old = correction_norm

    else:
        # solution not converged
        success = False
        # undo last update
        y0 += correction

    return PeriodicOutput(y0, success, residual, it, sol)
