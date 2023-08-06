import logging
import arklog
import rdflib
from rdflib import Literal
from rdflib.plugins.sparql.evalutils import _eval
from dataclasses import dataclass

from spendpoint.bridge import fetch_outliers
arklog.set_config_logging()


@dataclass(init=True, repr=True, order=False, frozen=True)
class Outlier:
    iri: str
    value: str

def outlier_service(query_results, ctx, part, eval_part):
    """

    Example query:
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX dtf:  <https://ontology.rys.app/dt/function/>
    PREFIX owl:  <http://www.w3.org/2002/07/owl#>

    SELECT ?outlier ?outlier_relation ?outlier_value WHERE {
      SERVICE <http://127.0.0.1:8000/> {
        SELECT ?outlier ?outlier_relation ?outlier_value WHERE {
          BIND(dtf:outlier("rotation.csv", "2", "<http://ua.be/drivetrain/description/artifacts/artifacts#drivetrain-sensor-data-v1>") AS ?outlier)
        }
      }
    }

    :param query_results:
    :param ctx:
    :param part:
    :param eval_part:
    :return:
    """
    logging.debug(f"Outlier service.")
    file_name = str(_eval(part.expr.expr[0], eval_part.forget(ctx, _except=part.expr._vars)))
    column = str(_eval(part.expr.expr[1], eval_part.forget(ctx, _except=part.expr._vars)))
    iri = str(_eval(part.expr.expr[2], eval_part.forget(ctx, _except=part.expr._vars)))
    logging.info(f"Looking for outlier in '{file_name}' at column '{column}' for '{iri}'.")
    outlier_graph = fetch_outliers(file_name, column, iri)
    for stmt in outlier_graph:
        query_results.append(eval_part.merge({
            part.var: stmt[0],
            rdflib.term.Variable(part.var + "_relation") : stmt[1],
            rdflib.term.Variable(part.var + "_value") : stmt[2],
        }))
    return query_results, ctx, part, eval_part


def example_service(query_results, ctx, part, eval_part):
    """"""
    logging.debug(f"{query_results=}")
    logging.debug(f"{ctx=}")
    logging.debug(f"{part=}")
    logging.debug(f"{eval_part=}")

    file_name = str(_eval(part.expr.expr[0], eval_part.forget(ctx, _except=part.expr._vars)))
    column = str(_eval(part.expr.expr[1], eval_part.forget(ctx, _except=part.expr._vars)))
    logging.info(f"Looking for outlier in '{file_name}' at column '{column}'.")

    outliers = [
        Outlier(iri="example_0",value="2.0"),
        Outlier(iri="example_1",value="2.5"),
        Outlier(iri="example_2",value="3.0"),
    ]

    for outlier in outliers:
        query_results.append(eval_part.merge({part.var: Literal(outlier.iri), rdflib.term.Variable(part.var + "_value"): Literal(outlier.value)}))
    return query_results, ctx, part, eval_part
