import arklog
from spendpoint.endpoint import SparqlEndpoint
from spendpoint import __version__
from spendpoint.service import outlier_service, example_service

arklog.set_config_logging()

app = SparqlEndpoint(
    version = __version__,
    functions = {
        "https://ontology.rys.app/dt/function/outlier": outlier_service,
        "https://ontology.rys.app/dt/function/example": example_service,
    },
    title = "SPARQL endpoint for storage and services",
    description = "/n".join(("SPARQL endpoint.",))
)
