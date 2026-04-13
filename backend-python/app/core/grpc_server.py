import grpc
from concurrent import futures
from app.core.config import settings


class AnalysisServicer:
    async def GetAnalysis(self, request, context):
        # gRPC service implementation
        pass


async def serve():
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    # Add servicer
    server.add_insecure_port(f'[::]:{settings.GRPC_PORT}')
    await server.start()
    await server.wait_for_termination()


async def start_grpc_server():
    await serve()