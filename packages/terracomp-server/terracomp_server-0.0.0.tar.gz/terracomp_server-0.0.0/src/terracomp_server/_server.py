import grpc

from ._project import ProjectService


class TerraformServer:
    def __init__(self) -> None:
        self._server = grpc.Server()
        self._server.add_generic_rpc_handlers()
