"""provider.py."""
import logging
from typing import List, Optional

import strangeworks
from qiskit import Aer
from qiskit.providers import ProviderV1 as Provider
from qiskit.providers.models import BackendConfiguration
from qiskit.providers.providerutils import filter_backends
from strangeworks.sw_client import SWClient as SDKClient

from strangeworks_qiskit._hw_api import SWClient
from strangeworks_qiskit._runtime_client import RuntimeClient
from strangeworks_qiskit.backends import backend_resolution, product_resolution
from strangeworks_qiskit.platform import backends as workspace_backends
from strangeworks_qiskit.runtimes import StrangeworksRuntimeService


class StrangeworksProvider(Provider):
    """The Strangeworks Provider allows access to Strangeworks backends and runtime
    wrappers for the Qiskit IBMQ Runtime services"""

    def __init__(
        self,
        client: Optional[SDKClient] = None,
    ):
        sdk_client = client or strangeworks.client
        self._sw = SWClient(sdk_client)
        self.sdk_client = sdk_client

        self._runtime = StrangeworksRuntimeService(
            provider=self, runtime_client=RuntimeClient(sdk_client)
        )
        self._backends = None

    def backends(self, name=None, filters=None, **kwargs):
        resources = self.sdk_client.resources()
        product_slugs = list(map(lambda x: x.product.slug, resources))
        if not self._backends:
            self._backends = self._discover_backends(product_slugs=product_slugs)

        backends = self._backends
        if name:
            backends = [b for b in backends if b.name() == name]

        return filter_backends(backends, filters, **kwargs)

    def _discover_backends(
        self,
        product_slugs: Optional[List[str]] = None,
    ):
        backends = []
        platform_backends = workspace_backends.get(
            self.sdk_client.backend_gql_client,
            statuses=["ONLINE"],
            product_slugs=product_slugs,
        )
        for be in platform_backends:
            if not be.properties:
                logging.debug(f"skipping {be.name} with config {be.properties}")
                continue

            cls, gates = product_resolution(be.product.slug, be.properties)
            if not cls:
                continue

            if gates:
                try:
                    conf = BackendConfiguration.from_dict(gates)
                    b = cls(
                        conf,
                        self,
                        be.name,
                        self._sw,
                        True,
                        None,
                        sw_product_info=be.product,
                        # sw_properties=be.properties,
                    )

                    backends.append(b)
                except TypeError as e:
                    logging.error(
                        f"error retrieving configuration info for backend {be.name}",
                        e,
                    )

        # we also support all of the aer backends!
        for b in Aer.backends():
            cls = backend_resolution(
                f"ibm.simulator.{b.name()}", b.configuration().to_dict()
            )
            if not cls:
                continue
            backends.append(
                cls(b.configuration(), self, b.name(), self._sw, False, {}, b)
            )

        return backends

    @property
    def runtime(self) -> StrangeworksRuntimeService:
        """Return the runtime service.
        Returns:
            The runtime service instance.
        Raises:
            IBMQNotAuthorizedError: If the account is not authorized to use the service.
        """
        if self._runtime:
            return self._runtime
        else:
            raise Exception("You are not authorized to use the runtime service.")


def get_backend(name=None, **kwargs):
    sw = StrangeworksProvider()
    return sw.get_backend(name, **kwargs)
