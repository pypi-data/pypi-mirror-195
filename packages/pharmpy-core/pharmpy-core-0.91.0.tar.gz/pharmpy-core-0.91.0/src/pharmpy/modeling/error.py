"""
:meta private:
"""
from __future__ import annotations

from typing import Optional, Union

from pharmpy.deps import sympy
from pharmpy.internals.expr.parse import parse as parse_expr
from pharmpy.internals.expr.subs import subs
from pharmpy.model import Assignment, Model, NormalDistribution, Statements

from .common import remove_unused_parameters_and_rvs
from .data import get_observations
from .expressions import create_symbol
from .parameters import add_population_parameter, fix_parameters, set_initial_estimates


def _preparations(model):
    stats = model.statements
    # FIXME: handle other DVs?
    y = list(model.dependent_variables.keys())[0]
    f = subs(
        model.statements.find_assignment(y.name).expression,
        {sympy.Symbol(eps): 0 for eps in model.random_variables.epsilons.names},
        simultaneous=True,
    )
    return stats, y, f


def _canonicalize_data_transformation(model, value):
    # FIXME: handle other DVs
    dv = list(model.dependent_variables.keys())[0]
    if value is None:
        value = dv
    else:
        value = parse_expr(value)
        if value.free_symbols != {dv}:
            raise ValueError(
                f"Expression for data transformation must contain the dependent variable "
                f"{dv} and no other variables"
            )
    return value


def remove_error_model(model: Model):
    """Remove error model.

    Parameters
    ----------
    model : Model
        Remove error model for this model

    Return
    ------
    Model
        Pharmpy model object

    Examples
    --------
    >>> from pharmpy.modeling import remove_error_model, load_example_model
    >>> model = load_example_model("pheno")
    >>> model.statements.find_assignment("Y")
    Y = EPS₁⋅W + F
    >>> model = remove_error_model(model)
    >>> model.statements.find_assignment("Y")
    Y = F

    Warnings
    --------
    Removing the error model will make the model unrunable for some tools.

    """
    stats, y, f = _preparations(model)
    model = model.replace(statements=stats.reassign(y, f))
    model = remove_unused_parameters_and_rvs(model)
    return model.update_source()


def set_additive_error_model(
    model: Model, data_trans: Optional[Union[str, sympy.Expr]] = None, series_terms: int = 2
):
    r"""Set an additive error model. Initial estimate for new sigma is :math:`(min(DV)/2)²`.

    The error function being applied depends on the data transformation. The table displays
    some examples.

    +------------------------+----------------------------------------+
    | Data transformation    | Additive error                         |
    +========================+========================================+
    | :math:`y`              | :math:`f + \epsilon_1`                 |
    +------------------------+----------------------------------------+
    | :math:`log(y)`         | :math:`\log(f) + \frac{\epsilon_1}{f}` |
    +------------------------+----------------------------------------+

    Parameters
    ----------
    model : Model
        Set error model for this model
    data_trans : str or expression
        A data transformation expression or None (default) to use the transformation
        specified by the model. Series expansion will be used for approximation.
    series_terms : int
        Number of terms to use for the series expansion approximation for data
        transformation.

    Return
    ------
    Model
        Pharmpy model object

    Examples
    --------
    >>> from pharmpy.modeling import set_additive_error_model, load_example_model
    >>> model = load_example_model("pheno")
    >>> model.statements.find_assignment("Y")
    Y = EPS₁⋅W + F
    >>> model = set_additive_error_model(model)
    >>> model.statements.find_assignment("Y")
    Y = F + εₐ

    >>> from pharmpy.modeling import set_additive_error_model, load_example_model
    >>> model = load_example_model("pheno")
    >>> model.statements.find_assignment("Y")
    Y = EPS₁⋅W + F
    >>> model = set_additive_error_model(model, data_trans="log(Y)")
    >>> model.statements.find_assignment("Y")
                 εₐ
        log(F) + ──
    Y =          F

    See Also
    --------
    set_proportional_error_model : Proportional error model
    set_combined_error_model : Combined error model

    """
    if has_additive_error_model(model):
        return model
    stats, y, f = _preparations(model)
    ruv = create_symbol(model, 'epsilon_a')

    data_trans = _canonicalize_data_transformation(model, data_trans)
    expr = f + ruv
    # FIXME: handle other DVs
    dv = list(model.dependent_variables.keys())[0]
    if data_trans != dv:
        expr = subs(data_trans, {dv: expr}, simultaneous=True).series(ruv, n=series_terms).removeO()

    model = model.replace(statements=stats.reassign(y, expr))
    model = remove_unused_parameters_and_rvs(model)

    sigma = create_symbol(model, 'sigma')
    model = add_population_parameter(model, sigma.name, _get_prop_init(model))

    eps = NormalDistribution.create(ruv.name, 'RUV', 0, sigma)
    model = model.replace(random_variables=model.random_variables + eps)
    return model.update_source()


def _get_prop_init(model):
    dv_min = get_observations(model).min()
    if dv_min == 0:
        return 0.01
    else:
        return (dv_min / 2) ** 2


def set_proportional_error_model(
    model: Model, data_trans: Optional[Union[str, sympy.Expr]] = None, zero_protection: bool = True
):
    r"""Set a proportional error model. Initial estimate for new sigma is 0.09.

    The error function being applied depends on the data transformation.

    +------------------------+----------------------------------------+
    | Data transformation    | Proportional error                     |
    +========================+========================================+
    | :math:`y`              | :math:`f + f \epsilon_1`               |
    +------------------------+----------------------------------------+
    | :math:`log(y)`         | :math:`\log(f) + \epsilon_1`           |
    +------------------------+----------------------------------------+

    Parameters
    ----------
    model : Model
        Set error model for this model
    data_trans : str or expression
        A data transformation expression or None (default) to use the transformation
        specified by the model.
    zero_protection : bool
        Set to True to add code protecting from IPRED=0

    Returns
    -------
    Model
        Pharmpy model object

    Examples
    --------
    >>> from pharmpy.modeling import *
    >>> model = remove_error_model(load_example_model("pheno"))
    >>> model = set_proportional_error_model(model)
    >>> model.statements.after_odes
        A_CENTRAL
        ─────────
    F =     S₁
    W = F
               ⎧2.225e-16  for F = 0
               ⎨
    IPREDADJ = ⎩    F      otherwise
    Y = F + IPREDADJ⋅εₚ
    IPRED = F
    IRES = DV - IPRED
            IRES
            ────
    IWRES =  W

    >>> from pharmpy.modeling import *
    >>> model = remove_error_model(load_example_model("pheno"))
    >>> model = set_proportional_error_model(
    ...     model,
    ...     data_trans="log(Y)"
    ... )
    >>> model.statements.after_odes
        A_CENTRAL
        ─────────
    F =     S₁
    W = F
               ⎧2.225e-16  for F = 0
               ⎨
    IPREDADJ = ⎩    F       otherwise
    Y = εₚ + log(IPREDADJ)
    IPRED = F
    IRES = DV - IPRED
            IRES
            ────
    IWRES =  W

    See Also
    --------
    set_additive_error_model : Additive error model
    set_combined_error_model : Combined error model

    """
    if has_proportional_error_model(model):
        return model

    stats, y, f = _preparations(model)
    ruv = create_symbol(model, 'epsilon_p')

    data_trans = _canonicalize_data_transformation(model, data_trans)
    ipred = create_symbol(model, 'IPREDADJ') if zero_protection else f

    # FIXME: handle other DVs
    dv = list(model.dependent_variables.keys())[0]
    if data_trans == sympy.log(dv):
        expr = sympy.log(ipred) + ruv
    elif data_trans == dv:
        expr = f + ipred * ruv
    else:
        raise ValueError(f"Not supported data transformation {data_trans}")

    statements = model.statements
    if zero_protection:
        guard_expr = sympy.Piecewise((2.225e-16, sympy.Eq(f, 0)), (f, True))
        guard_assignment = Assignment(ipred, guard_expr)
        ind = stats.find_assignment_index(y)
        statements = statements[0:ind] + guard_assignment + statements[ind:]

    model = model.replace(statements=statements.reassign(y, expr))
    model = remove_unused_parameters_and_rvs(model)

    sigma = create_symbol(model, 'sigma')
    model = add_population_parameter(model, sigma.name, 0.09)

    eps = NormalDistribution.create(ruv.name, 'RUV', 0, sigma)
    model = model.replace(random_variables=model.random_variables + eps)
    model = model.update_source()
    return model


def set_combined_error_model(model: Model, data_trans: Optional[Union[str, sympy.Expr]] = None):
    r"""Set a combined error model. Initial estimates for new sigmas are :math:`(min(DV)/2)²` for
    proportional and 0.09 for additive.

    The error function being applied depends on the data transformation.

    +------------------------+-----------------------------------------------------+
    | Data transformation    | Combined error                                      |
    +========================+=====================================================+
    | :math:`y`              | :math:`f + f \epsilon_1 + \epsilon_2`               |
    +------------------------+-----------------------------------------------------+
    | :math:`log(y)`         | :math:`\log(f) + \epsilon_1 + \frac{\epsilon_2}{f}` |
    +------------------------+-----------------------------------------------------+

    Parameters
    ----------
    model : Model
        Set error model for this model
    data_trans : str or expression
        A data transformation expression or None (default) to use the transformation
        specified by the model.

    Return
    ------
    Model
        Pharmpy model object

    Examples
    --------
    >>> from pharmpy.modeling import *
    >>> model = remove_error_model(load_example_model("pheno"))
    >>> model = set_combined_error_model(model)
    >>> model.statements.find_assignment("Y")
    Y = F⋅εₚ + F + εₐ

    >>> from pharmpy.modeling import *
    >>> model = remove_error_model(load_example_model("pheno"))
    >>> model = set_combined_error_model(model, data_trans="log(Y)")
    >>> model.statements.find_assignment("Y")
                     εₐ
       εₚ + log(F) + ──
    Y =              F

    See Also
    --------
    set_additive_error_model : Additive error model
    set_proportional_error_model: Proportional error model

    """
    if has_combined_error_model(model):
        return model
    stats, y, f = _preparations(model)

    expr = stats.find_assignment(y.name).expression

    ruv_prop = create_symbol(model, 'epsilon_p')
    ruv_add = create_symbol(model, 'epsilon_a')

    eta_ruv = sympy.Symbol('ETA_RV1')
    theta_time = sympy.Symbol('time_varying')

    data_trans = _canonicalize_data_transformation(model, data_trans)

    # FIXME: handle other DVs
    dv = list(model.dependent_variables.keys())[0]
    if data_trans == sympy.log(dv):
        expr_combined = sympy.log(f) + ruv_prop + ruv_add / f
    elif data_trans == dv:
        if isinstance(expr, sympy.Piecewise):
            expr_0 = expr.args[0][0]
            expr_1 = expr.args[1][0]
            cond_0 = expr.args[0][1]
            expr_combined = None
            for eps in model.random_variables.epsilons.names:
                expr_0 = subs(expr_0, {sympy.Symbol(eps): ruv_prop}, simultaneous=True)
                expr_1 = subs(expr_1, {sympy.Symbol(eps): ruv_prop}, simultaneous=True)
                if (
                    eta_ruv in model.random_variables.free_symbols
                    and theta_time in model.parameters.symbols
                ):
                    expr_combined = sympy.Piecewise(
                        (expr_0 + ruv_add * theta_time * sympy.exp(eta_ruv), cond_0),
                        (expr_1 + ruv_add * sympy.exp(eta_ruv), True),
                    )
                elif (
                    eta_ruv not in model.random_variables.free_symbols
                    and theta_time in model.parameters.symbols
                ):
                    expr_combined = sympy.Piecewise(
                        (expr_0 + ruv_add * theta_time, cond_0), (expr_1 + ruv_add, True)
                    )
            assert expr_combined is not None
        elif (
            eta_ruv in model.random_variables.free_symbols
            and theta_time not in model.parameters.symbols
        ):
            expr_combined = f + f * ruv_prop * sympy.exp(eta_ruv) + ruv_add * sympy.exp(eta_ruv)
        else:
            expr_combined = f + f * ruv_prop + ruv_add
    else:
        raise ValueError(f"Not supported data transformation {data_trans}")

    model = model.replace(statements=stats.reassign(y, expr_combined))
    model = remove_unused_parameters_and_rvs(model)

    sigma_prop = create_symbol(model, 'sigma_prop')
    model = add_population_parameter(model, sigma_prop.name, 0.09)
    sigma_add = create_symbol(model, 'sigma_add')
    model = add_population_parameter(model, sigma_add.name, _get_prop_init(model))

    eps_prop = NormalDistribution.create(ruv_prop.name, 'RUV', 0, sigma_prop)
    eps_add = NormalDistribution.create(ruv_add.name, 'RUV', 0, sigma_add)
    model = model.replace(random_variables=model.random_variables + [eps_prop, eps_add])
    return model.update_source()


def has_additive_error_model(model: Model):
    """Check if a model has an additive error model

    Parameters
    ----------
    model : Model
        The model to check

    Return
    ------
    bool
        True if the model has an additive error model and False otherwise

    Examples
    --------
    >>> from pharmpy.modeling import load_example_model, has_additive_error_model
    >>> model = load_example_model("pheno")
    >>> has_additive_error_model(model)
    False

    See Also
    --------
    has_proportional_error_model : Check if a model has a proportional error model
    has_combined_error_model : Check if a model has a combined error model
    has_weighted_error_model : Check if a model has a weighted error model
    """
    # FIXME: handle other DVs
    y = list(model.dependent_variables.keys())[0]
    expr = model.statements.error.full_expression(y)
    rvs = model.random_variables.epsilons
    rvs_in_y = {sympy.Symbol(name) for name in rvs.names if sympy.Symbol(name) in expr.free_symbols}
    if len(rvs_in_y) != 1:
        return False
    eps = rvs_in_y.pop()
    return eps not in (expr - eps).simplify().free_symbols


def has_proportional_error_model(model: Model):
    """Check if a model has a proportional error model

    Parameters
    ----------
    model : Model
        The model to check

    Return
    ------
    bool
        True if the model has a proportional error model and False otherwise

    Examples
    --------
    >>> from pharmpy.modeling import load_example_model, has_proportional_error_model
    >>> model = load_example_model("pheno")
    >>> has_proportional_error_model(model)
    True

    See Also
    --------
    has_additive_error_model : Check if a model has an additive error model
    has_combined_error_model : Check if a model has a combined error model
    has_weighted_error_model : Check if a model has a weighted error model
    """
    # FIXME: handle other DVs
    y = list(model.dependent_variables.keys())[0]
    expr = model.statements.error.full_expression(y)
    rvs = model.random_variables.epsilons
    rvs_in_y = {sympy.Symbol(name) for name in rvs.names if sympy.Symbol(name) in expr.free_symbols}
    if len(rvs_in_y) != 1:
        return False
    eps = rvs_in_y.pop()
    return eps not in (expr / (1 + eps)).simplify().free_symbols


def has_combined_error_model(model: Model):
    """Check if a model has a combined additive and proportinal error model

    Parameters
    ----------
    model : Model
        The model to check

    Return
    ------
    bool
        True if the model has a combined error model and False otherwise

    Examples
    --------
    >>> from pharmpy.modeling import load_example_model, has_combined_error_model
    >>> model = load_example_model("pheno")
    >>> has_combined_error_model(model)
    False

    See Also
    --------
    has_additive_error_model : Check if a model has an additive error model
    has_proportional_error_model : Check if a model has a proportional error model
    has_weighted_error_model : Check if a model has a weighted error model
    """
    # FIXME: handle other DVs
    y = list(model.dependent_variables.keys())[0]
    expr = model.statements.error.full_expression(y)
    rvs = model.random_variables.epsilons
    rvs_in_y = {sympy.Symbol(name) for name in rvs.names if sympy.Symbol(name) in expr.free_symbols}
    if len(rvs_in_y) != 2:
        return False
    eps1 = rvs_in_y.pop()
    eps2 = rvs_in_y.pop()
    canc1 = ((expr - eps1) / (eps2 + 1)).simplify()
    canc2 = ((expr - eps2) / (eps1 + 1)).simplify()
    return (
        eps1 not in canc1.free_symbols
        and eps2 not in canc1.free_symbols
        or eps1 not in canc2.free_symbols
        and eps2 not in canc2.free_symbols
    )


def use_thetas_for_error_stdev(model: Model):
    """Use thetas to estimate standard deviation of error

    Parameters
    ----------
    model : Model
        Pharmpy model

    Return
    ------
    Model
        Pharmpy model object

    Examples
    --------
    >>> from pharmpy.modeling import load_example_model, use_thetas_for_error_stdev
    >>> model = load_example_model("pheno")
    >>> model = use_thetas_for_error_stdev(model)
    >>> model.statements.find_assignment("Y")
    Y = EPS₁⋅SD_EPS_1⋅W + F

    See also
    --------
    set_weighted_error_model : Encode error model with one epsilon and weight
    """
    rvs = model.random_variables.epsilons
    for eps in rvs:
        sigmas = eps.parameter_names
        if len(sigmas) > 1:
            raise ValueError('use_thetas_for_error_stdev only supports non-correlated sigmas')
        sigma = sigmas[0]

        param = model.parameters[sigma]
        theta_init = param.init**0.5
        model = fix_parameters(model, [sigma])
        model = set_initial_estimates(model, {sigma: 1})

        sdsymb = create_symbol(model, f'SD_{eps.names[0]}')
        model = add_population_parameter(model, sdsymb.name, theta_init, lower=0)
        symb = sympy.Symbol(eps.names[0])
        model = model.replace(statements=model.statements.subs({symb: sdsymb * symb}))
    return model.update_source()


def set_weighted_error_model(model: Model):
    """Encode error model with one epsilon and W as weight

    Parameters
    ----------
    model : Model
        Pharmpy model

    Return
    ------
    Model
        Pharmpy model object

    Examples
    --------
    >>> from pharmpy.modeling import load_example_model, set_weighted_error_model
    >>> model = load_example_model("pheno")
    >>> model = set_weighted_error_model(model)

    See also
    --------
    use_thetas_for_error_stdev : Use thetas to estimate error
    """
    stats, y, f = _preparations(model)
    epsilons = model.random_variables.epsilons
    expr = stats.find_assignment(y.name).expression
    ssum = 0
    q = sympy.Q.real(y)  # Dummy predicate
    for term in expr.args:
        eps = [x for x in term.free_symbols if x.name in epsilons.names]
        if len(eps) > 0:
            eps = eps[0]
            remaining = term / eps
            ssum += remaining**2
            for symb in remaining.free_symbols:
                q &= sympy.Q.positive(symb)
    w = sympy.sqrt(ssum)
    w = sympy.refine(w, q)

    i = _index_of_first_assignment(stats, y)

    model = model.replace(statements=stats[0:i] + Assignment(sympy.Symbol('W'), w) + stats[i:])
    model = model.replace(
        statements=model.statements.reassign(
            y, f + sympy.Symbol('W') * sympy.Symbol(epsilons[0].names[0])
        )
    )
    model = remove_unused_parameters_and_rvs(model)
    return model.update_source()


def has_weighted_error_model(model: Model):
    """Check if a model has a weighted error model

    Parameters
    ----------
    model : Model
        The model to check

    Return
    ------
    bool
        True if the model has a weighted error model and False otherwise

    Examples
    --------
    >>> from pharmpy.modeling import load_example_model, has_weighted_error_model
    >>> model = load_example_model("pheno")
    >>> has_weighted_error_model(model)
    True

    See Also
    --------
    has_additive_error_model : Check if a model has an additive error model
    has_combined_error_model : Check if a model has a combined error model
    has_proportional_error_model : Check if a model has a proportional error model
    """
    stats, y, f = _preparations(model)
    y_expr = stats.error.find_assignment(y).expression
    rvs = model.random_variables.epsilons
    rvs_in_y = {
        sympy.Symbol(name) for name in rvs.names if sympy.Symbol(name) in y_expr.free_symbols
    }

    if len(rvs_in_y) > 1:
        return False
    eps_expr = {arg for arg in y_expr.args if arg.free_symbols.intersection(rvs_in_y)}
    if not eps_expr:
        return False

    # FIXME: this only covers the simple case of e.g. Y=CONC+W*EPS(1)
    eps_expr = eps_expr.pop()
    if len(eps_expr.args) == 2 and eps_expr.func is sympy.Mul:
        a, b = eps_expr.args
        w_cand = a if a not in rvs_in_y else b
        if w_cand not in y_expr.args:
            return True
    return False


def _index_of_first_assignment(statements: Statements, symbol: sympy.Symbol) -> int:
    return next(
        (i for i, s in enumerate(statements) if isinstance(s, Assignment) and s.symbol == symbol)
    )


def set_dtbs_error_model(model: Model, fix_to_log: bool = False):
    """Dynamic transform both sides

    Parameters
    ----------
    model : Model
        Pharmpy model
    fix_to_log : Boolean
        Set to True to fix lambda and zeta to 0, i.e. emulating log-transformed data

    Return
    ------
    Model
        Pharmpy model object

    Examples
    --------
    >>> from pharmpy.modeling import load_example_model, set_dtbs_error_model
    >>> model = load_example_model("pheno")
    >>> model = set_dtbs_error_model(model)

    """
    model = use_thetas_for_error_stdev(model)
    model = set_weighted_error_model(model)
    stats, y, f = _preparations(model)
    lam = create_symbol(model, 'tbs_lambda')
    zeta = create_symbol(model, 'tbs_zeta')
    if fix_to_log:
        model = add_population_parameter(model, lam.name, 0, fix=True)
        model = add_population_parameter(model, zeta.name, 0, fix=True)
    else:
        model = add_population_parameter(model, lam.name, 1)
        model = add_population_parameter(model, zeta.name, 0.001)

    i = _index_of_first_assignment(stats, sympy.Symbol('W'))

    wass = Assignment(sympy.Symbol('W'), (f**zeta) * sympy.Symbol('W'))
    ipred = sympy.Piecewise(
        ((f**lam - 1) / lam, sympy.And(sympy.Ne(lam, 0), sympy.Ne(f, 0))),
        (sympy.log(f), sympy.And(sympy.Eq(lam, 0), sympy.Ne(f, 0))),
        (-1 / lam, sympy.And(sympy.Eq(lam, 0), sympy.Eq(f, 0))),
        (-1000000000, True),
    )
    ipredass = Assignment(sympy.Symbol('IPRED'), ipred)
    yexpr_ind = stats.find_assignment_index(y.name)
    yexpr = stats[yexpr_ind].subs({f: sympy.Symbol('IPRED')})

    statements = (
        stats[0 : i + 1]
        + wass
        + ipredass
        + stats[i + 1 : yexpr_ind]
        + yexpr
        + stats[yexpr_ind + 1 :]
    )

    obs = sympy.Piecewise(
        (sympy.log(y), sympy.Eq(lam, 0)), ((y**lam - 1) / lam, sympy.Ne(lam, 0))
    )
    model = model.replace(observation_transformation=obs, statements=statements)

    return model.update_source()


def set_time_varying_error_model(model: Model, cutoff: float, idv: str = 'TIME'):
    """Set a time varying error model per time cutoff

    Parameters
    ----------
    model : Model
        Pharmpy model
    cutoff : float
        A value at the given quantile over idv column
    idv : str
        Time or time after dose, default is Time

    Return
    ------
    Model
        Pharmpy model object

    Examples
    --------
    >>> from pharmpy.modeling import load_example_model, set_time_varying_error_model
    >>> model = load_example_model("pheno")
    >>> model = set_time_varying_error_model(model, cutoff=1.0)
    >>> model.statements.find_assignment("Y")
        ⎧EPS₁⋅W⋅time_varying + F  for TIME < 1.0
        ⎨
    Y = ⎩      EPS₁⋅W + F           otherwise

    """
    y = model.statements.find_assignment('Y')
    idv = parse_expr(idv)
    theta = create_symbol(model, 'time_varying')
    eps = model.random_variables.epsilons
    expr = sympy.Piecewise(
        (
            subs(
                y.expression,
                {sympy.Symbol(e): sympy.Symbol(e) * theta for e in eps.names},
                simultaneous=True,
            ),
            idv < cutoff,
        ),
        (y.expression, True),
    )
    model = model.replace(statements=model.statements.reassign(y.symbol, expr))
    model = add_population_parameter(model, theta.name, 0.1)
    return model.update_source()
