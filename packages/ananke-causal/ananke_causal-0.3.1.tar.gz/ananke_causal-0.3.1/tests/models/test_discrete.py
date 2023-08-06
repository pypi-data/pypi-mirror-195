import pytest
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination
from pgmpy.models import BayesianNetwork

from ananke.graphs import ADMG
from ananke.identification import OneLineID
from ananke.models import discrete


def test_estimate_effect_from_distribution():
    di_edges = [("A", "Y"), ("C", "A"), ("C", "Y")]
    graph = ADMG(["A", "C", "Y"], di_edges=di_edges)
    net = BayesianNetwork(di_edges)
    net = net.get_random_cpds(n_states=2)
    treatment_dict = {"A": 1}
    outcome_dict = {"Y": 1}

    int_net = discrete.intervene(net, treatment_dict)
    int_inference = VariableElimination(int_net)
    truth = int_inference.query(["Y"]).get_value(**outcome_dict)

    oid = OneLineID(graph, list(treatment_dict), list(outcome_dict))
    effect = discrete.estimate_effect_from_discrete(
        oid, net, treatment_dict, outcome_dict
    )

    assert truth == pytest.approx(effect)
