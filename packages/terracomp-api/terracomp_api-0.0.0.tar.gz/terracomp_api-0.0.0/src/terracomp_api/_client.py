from typing import Sequence

import grpc

from ._interceptor import TokenInterceptor
from .grpc import terracomp as api


class TerracompClient:
    """
    High-level client wrapping the Terracomp GRPC API.
    """

    def __init__(self, host: str, port: int, token: str, timeout: float | None = None) -> None:
        self._channel = grpc.intercept_channel(grpc.Channel(host, port), TokenInterceptor(token))
        self._projects = api.ProjectServiceStub(self._channel, timeout=timeout)
        self._runs = api.RunServiceStub(self._channel, timeout=timeout)
        self._state = api.StateServiceStub(self._channel, timeout=timeout)

    async def list_projects(self) -> list[api.Project]:
        return (await self._projects.list_projects()).projects

    async def create_project(self, name: str, description: str = "", tags: Sequence[str] = ()) -> api.Project:
        return await self._projects.create_project(name=name, description=description, tags=list(tags))

    async def update_project(self, name: str, description: str = "", tags: Sequence[str] = ()) -> api.Project:
        return await self._projects.update_project(name=name, description=description, tags=list(tags))

    async def delete_project(self, project: str) -> None:
        await self._projects.delete_project(project)

    async def list_states(
        self, project: str, environment: str | None = None, page_token: str | None = None
    ) -> tuple[list[api.StateMetadata], str | None]:
        response = await self._state.list_states(project=project, environment=environment, page_token=page_token)
        return response.states, response.next_page_token

    async def get_state(self, project: str, environment: str, version: int) -> api.State:
        return await self._state.get_state(project=project, environment=environment, version=int)

    # TODO
    # async def append_state(self, project: str, environment: str, )
