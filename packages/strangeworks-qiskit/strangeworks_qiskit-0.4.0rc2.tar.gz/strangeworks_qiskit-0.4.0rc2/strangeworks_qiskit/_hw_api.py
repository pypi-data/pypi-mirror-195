"""_hw_api.py."""

from strangeworks.sw_client import SWClient as SDKClient


class SWClient:
    def __init__(self, client: SDKClient):
        self.__client = client
        self.__base_url = "/qiskit"

    def create_job(self, input, backend_name: str, backend_product_slug: str, **kwargs):
        # retrieve corresponding resource.
        existing_resources = self.__client.resources()
        product_resources = [
            x for x in existing_resources if x.product.slug == backend_product_slug
        ]

        if not product_resources or len(product_resources) == 0:
            # TODO: make this an exception.
            print(f"please create a resource for {backend_product_slug}")
            return

        # Pick the first one for now. throw ex if there is more than one.
        resource = product_resources[0]

        circuit_type = type(input).__name__
        payload = {
            "qobj_dict": input.to_dict(),
            "circuit_type": circuit_type,
            "backend_name": backend_name,
        }
        payload.update(kwargs)
        return self.__client.execute(
            res=resource, payload=payload, endpoint="create_job"
        )

    def cancel_job(self, job_slug: str, product_slug: str):
        pass

    def fetch_job(self, job_id):
        url = f"{self.__base_url}/fetch-job"
        url += f"?job_id={job_id}"
        return self.__client.rest_client.get(url)

    def get_job_status(self, job_id):
        pass

    def fetch_backend_status(self, account_slug, backend_name):
        if account_slug:
            self.__client.rest_client.headers[
                "x-strangeworks-provider-account"
            ] = account_slug
        url = f"{self.__base_url}/backend/{backend_name}/status"
        return self.__client.rest_client.get(url)

    def fetch_backend_properties(self, account_slug, backend_name):
        if account_slug:
            self.__client.rest_client.headers[
                "x-strangeworks-provider-account"
            ] = account_slug
        url = f"{self.__base_url}/backend/{backend_name}/properties"
        return self.__client.rest_client.get(url)
