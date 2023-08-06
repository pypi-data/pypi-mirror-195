import functools
from collections import ChainMap

import numpy as np
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination


def intervene(net, treatment_dict):
    """
    Performs an intervention on a pgmpy.models.BayesianNetwork, by setting the conditional distribution of
    each intervened variable to be a point mass at the intervened value. Does not alter the structure of the parents of the network (i.e. is a non-faithful operation).


    :param net: Bayesian Network
    :type net: pgmpy.models.BayesianNetwork
    :param treatment_dict: dictionary of variables to values:
    :type treatment_dict: dict


    """
    net_copy = net.copy()

    for vertex, value in treatment_dict.items():
        old_cpd = net_copy.get_cpds(vertex)
        old_values = old_cpd.get_values()
        new_values = np.zeros(old_values.shape)
        new_values[value, :] = 1
        new_cpd = TabularCPD(
            variable=vertex,
            variable_card=old_cpd.variable_card,
            values=new_values,
            evidence=old_cpd.variables[1:],
            evidence_card=old_cpd.cardinality[1:],
        )
        net_copy.add_cpds(new_cpd)

    return net_copy


def estimate_effect_from_discrete(oid, net, treatment_dict, outcome_dict):
    """
    Performs the ID algorithm to identify a causal effect given a discrete
    probability distribution representing the observed data distribution.

    :param oid: Ananke OneLineID object
    :param net: pgmpy.BayesianNetwork-like object
    :param treatment_dict: dictionary of treatment variables and values
    :param outcome_dict: dictionary of outcome variables and values
    """
    if not oid.id():
        return None

    factors = list()
    for district in sorted(oid.Gystar.districts):
        fixing_order = oid.fixing_orders[tuple(district)]
        factors.append(compute_district_factor(oid.graph, net, fixing_order))

    intervened_distribution = functools.reduce(
        (lambda first, last: first.product(last, inplace=False)), factors
    )

    # construct the variable tuples here using itertools.product (Y* - Y) with A = a
    summed_vars = oid.ystar - set(outcome_dict)

    # compute the causal effect

    causal_effect = intervened_distribution.marginalize(
        summed_vars, inplace=False
    ).get_value(**dict(ChainMap(treatment_dict, outcome_dict)))

    return causal_effect


def compute_district_factor(graph, net, fixing_order):
    """
    Compute the interventional distribution associated with a district (or equivalently, its fixing order)

    :param graph: Graph representing the problem
    :type graph: ananke.ADMG
    :param net: Probability distribution corresponding to the graph
    :type net: pgmpy.models.BayesianNetwork
    :param fixing_order: A fixing sequence for the implied district D
    """
    inference = VariableElimination(net)
    new_graph = graph.copy()
    curr_factor = inference.query(graph.vertices)
    for var in fixing_order:
        non_descendants = list(
            set(new_graph.vertices) - set(new_graph.descendants(var))
        )
        div_joint = curr_factor.marginalize(
            set(graph.descendants(var)) - {var}, inplace=False
        )
        if non_descendants:
            div_cond = div_joint.marginalize([var], inplace=False)
            div_factor = div_joint.divide(div_cond, inplace=False)
        else:
            div_factor = div_joint
        new_graph = new_graph.fix(var)

        curr_factor = curr_factor.divide(div_factor, inplace=False)
    return curr_factor
