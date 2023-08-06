"""client.py."""
import importlib.metadata
import os
from functools import singledispatchmethod
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urljoin

from strangeworks.core.client import file, jobs, platform, resource, workspace
from strangeworks.core.client.backends import Backend, get_backend, get_backends
from strangeworks.core.client.file import File
from strangeworks.core.client.jobs import Job
from strangeworks.core.client.resource import Resource
from strangeworks.core.client.rest_client import StrangeworksRestClient
from strangeworks.core.client.workspace import Workspace
from strangeworks.core.config.base import ConfigSource
from strangeworks.core.errors.error import StrangeworksError

__version__ = importlib.metadata.version("strangeworks")


class SWClient:
    """Strangeworks client object."""

    def __init__(
        self,
        cfg: ConfigSource,
        headers: Optional[Dict[str, str]] = None,
        rest_client: Optional[StrangeworksRestClient] = None,
        sdk_api: Optional[platform.API] = None,
        platform_api: Optional[platform.API] = None,
        **kwargs,
    ) -> None:
        """Strangeworks client.

        Implements the Strangeworks API and provides core functionality for cross-vendor
        applications.

        Parameters
        ----------
        cfg: ConfigSource
            Source for retrieving SDK configuration values.
        headers : Optional[Dict[str, str]]
            Headers that are sent as part of the request to Strangeworks.
        rest_client : Optional[StrangeworksRestClient]
        **kwargs
            Other keyword arguments to pass to tools like ``requests``.
        """
        self.cfg = cfg
        self.kwargs = kwargs

        self.headers = (
            os.getenv("STRANGEWORKS_HEADERS", default=None)
            if headers is None
            else headers
        )

        self.rest_client = rest_client
        self.gql_client = sdk_api
        self.backend_gql_client = platform_api

    def authenticate(
        self,
        api_key: Optional[str] = None,
        url: Optional[str] = None,
        profile: Optional[str] = None,
        store_credentials: bool = True,
        overwrite: bool = False,
        **kwargs,
    ) -> None:
        """Authenticate with Strangeworks.

        Obtains an authorization token from the platform using the api_key. The auth
        token is used to make calls to the platform. Access to platform interfaces
        are initialized.

        Parameters
        ----------
        api_key : Optional[str]
            The API key.
        url: Optional[str]
            The base URL to the Strangeworks API.
        profile: Optional[str]
            The profile name to use for configuration.
        store_credentials: bool
            Indicates whether credentials (api key an url)  should be saved. Defaults
            to True.
        overwrite: bool
            Indicates whether to overwrite credentials if they already exist. Defaults
            to False.
        **kwargs
            Additional arguments.
        """
        key = api_key or self.cfg.get("api_key")

        if key is None:
            raise StrangeworksError.authentication_error(
                message="Unable to retrieve api key from a previous configuration. Please provide your api_key."
            )

        # create new clients w/ auth in place
        self.gql_client = platform.API(
            api_key=key,
            base_url=url or self.cfg.get("url"),
            api_id=platform.APIName.SDK,
        )

        self.backend_gql_client = platform.API(
            api_key=key,
            base_url=url or self.cfg.get("url"),
            api_id=platform.APIName.PLATFORM,
        )

        self.rest_client = StrangeworksRestClient(
            api_key=key, host=url or self.cfg.get("url")
        )

        # if we made it this far, lets go ahead and try to save the configuration to a
        # file. But only if an api_key was provided.
        if api_key and store_credentials:
            self.cfg.set(
                profile=profile,
                overwrite=overwrite,
                api_key=api_key,
                url=self.cfg.get("url"),
            )

    def resources(self, slug: Optional[str] = None) -> Optional[List[Resource]]:
        """Retrieve list of resources that are available for this workspace account.

        Parameters
        ----------
        slug: Optional[str]
            Identifier for a specific resource. Defaults to None.

        Return
        ------
        Optional[List[Resource]]
            List of resources for the current workspace account or None if no resources
            have been created.
        """
        return resource.get(client=self.gql_client, resource_slug=slug)

    def jobs(
        self,
        slug: Optional[str] = None,
        resource_slugs: Optional[List[str]] = None,
        product_slugs: Optional[List[str]] = None,
        statuses: Optional[List[str]] = None,
    ) -> Job:
        """Retrieve list of jobs associated with the current workspace account.

        Parameters
        ----------
        slug : Optional[str] = None
            Identifier for a specific job. Defaults to None.
        resource_slugs: Optional[List[str]]
            List of resource identifiers. Only jobs whose resources match will be
            returned. Defaults to None.
        product_slugs: Optional[List[str]]
            List of product identifiers. Only jobs whose product slugs match will be
            returned. Defaults to None.
        statuses: Optional[List[str]]
            List of job statuses. Only obs whose statuses match will be returned.
            Defaults to None.

        Return
        -------
        : Optional[List[Job]]
            List of jobs or None if there are no jobs that match selection criteria.
        """
        return jobs.get(
            client=self.gql_client,
            job_slug=slug,
            product_slugs=product_slugs or [],
            resource_slugs=resource_slugs or [],
            statuses=statuses or [],
        )

    def workspace_info(self) -> Workspace:
        """Retrieve information about the current workspace."""
        return workspace.get(self.gql_client)

    def execute(
        self,
        res: resource.Resource,
        payload: Optional[Dict[str, Any]] = None,
        endpoint: Optional[str] = None,
    ):
        """Execute a job request.

        Parameters
        ----------
        res: resource.Resource
            the resource that has the function to call.
        payload: Optiona;[Dict[str, Any]]
            the payload to send with the request.
        endpoint:
            additional endpoint to append to the proxy path for the resource.

        """
        url = urljoin(res.proxy_url(), endpoint) if endpoint else res.proxy_url()

        if payload:
            return self.rest_client.post(
                url=url,
                json=payload,
            )

        return self.rest_client.get(url=url)

    def get_backends(
        self,
        product_slugs: List[str] = None,
        backend_type_slugs: List[str] = None,
        backend_statuses: List[str] = None,
        backend_tags: List[str] = None,
    ) -> List[Backend]:
        """Return a list of backends available based on the filters provided.

        Replaces the deprecated BackendsService.
        """
        return get_backends(
            client=self.backend_gql_client,
            product_slugs=product_slugs,
            backend_type_slugs=backend_type_slugs,
            backend_statuses=backend_statuses,
            backend_tags=backend_tags,
        )

    def get_backend(self, backend_slug: str) -> Backend:
        """Return a single backend by the slug.

        Replaces the deprecated BackendsService.
        """
        return get_backend(self.gql_client, backend_slug)

    def upload_file(self, file_path: str) -> File:
        """Upload a file to strangeworks.

        File.url is how you can download the file.

        raises StrangeworksError if any issues arise while attempting to upload the file.
        """
        w = workspace.get(self.gql_client)
        f, signedUrl = file.upload(self.gql_client, w.slug, file_path)
        try:
            fd = open(file_path, "rb")
        except IOError as e:
            raise StrangeworksError(f"unable to open {file_path}: {str(e)}")
        else:
            with fd:
                self.rest_client.put(signedUrl, data=fd)
        return f

    @singledispatchmethod
    def download_job_files(
        self,
        file_paths: Union[str, list],
        resource_slugs: Optional[List[str]] = None,
        product_slugs: Optional[List[str]] = None,
        statuses: Optional[List[str]] = None,
    ) -> List[File]:
        raise NotImplementedError("files must either be a string or a List of strings")

    @download_job_files.register
    def _(
        self,
        file_paths: str,
        resource_slugs: Optional[List[str]] = None,
        product_slugs: Optional[List[str]] = None,
        statuses: Optional[List[str]] = None,
    ) -> List[File]:
        sw_job = jobs.get(
            client=self.gql_client,
            job_slug=file_paths,
            product_slugs=product_slugs,
            resource_slugs=resource_slugs,
            statuses=statuses,
        )

        file_paths = [f.url for f in sw_job[0].files]

        files_out = [self.rest_client.get(url=f) for f in file_paths]

        return files_out

    @download_job_files.register
    def _(
        self,
        file_paths: list,
        resource_slugs: Optional[List[str]] = None,
        product_slugs: Optional[List[str]] = None,
        statuses: Optional[List[str]] = None,
    ) -> List[File]:

        files_out = [self.rest_client.get(url=f) for f in file_paths]

        return files_out
