from typing import Any, Dict

from strangeworks_qiskit.backends._utils import get_provider_and_account
from strangeworks_qiskit.backends.aws import AwsSimulator, GeneralAWSBackend
from strangeworks_qiskit.backends.honeywell import HoneywellBackend
from strangeworks_qiskit.backends.ibm import IBMQBackend, IBMQSimulator
from strangeworks_qiskit.backends.ionq import IonqBackend
from strangeworks_qiskit.backends.rigetti import RigettiBackend
from strangeworks_qiskit.backends.strangeworks import StrangeworksBackend


def get_backend_class(
    product: str, is_simulator: bool = False
) -> "StrangeworksBackend":
    _lowercase_product = product.lower()
    if "ibm" in _lowercase_product:
        return IBMQSimulator if is_simulator else IBMQBackend

    return None


def product_resolution(product_slug: str, cfg: Dict[str, Any]):
    simulator = cfg.get("simulator", False)
    if product_slug == "ibm-quantum":
        backend_class = IBMQSimulator if simulator else IBMQBackend
        if cfg.get("gates"):
            return backend_class, cfg

        props = cfg.get("capabilities")
        if props:
            has_gates = props.get("gates")
            if has_gates:
                return backend_class, props

        return IBMQBackend, None
    if product_slug == "rigetti":
        return RigettiBackend, None
    if product_slug == "amazon-braket":
        return None, None
    return None, None


def backend_resolution(
    sw_backend_name: str, backend_config: dict
) -> "StrangeworksBackend":
    provider, _ = get_provider_and_account(sw_backend_name)
    if not provider:
        return None

    simulator = False
    if "simulator" in backend_config:
        simulator = backend_config["simulator"]

    if provider == "ibm":
        if simulator:
            return IBMQSimulator
        return IBMQBackend

    if provider == "azure":
        if "honeywell" in sw_backend_name:
            return HoneywellBackend

        if "ionq" in sw_backend_name:
            return IonqBackend

    if provider == "aws":
        if "ionq" in sw_backend_name.lower():
            return IonqBackend
        if "aspen" in sw_backend_name.lower():
            return RigettiBackend
        if (
            "sv1" in sw_backend_name.lower()
            or "tn1" in sw_backend_name.lower()
            or "dm1" in sw_backend_name.lower()
        ):
            return AwsSimulator

        return GeneralAWSBackend

    if provider == "rigetti":
        return RigettiBackend

    return None
