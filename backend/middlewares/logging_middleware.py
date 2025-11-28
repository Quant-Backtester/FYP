import time
import uuid
import json
from fastapi import Request, Response
from configs import get_logger


class LoggingMiddleware:
    def __init__(self) -> None:
        pass
        
    async def __call__(self, request: Request, call_next):
        request_id = self._get_or_create_request_id(request=request)
        client_ip = self._get_client_ip(request=request)
        body_json = await self._read_body_safely(request=request)
        start_time = time.perf_counter()
        logger = get_logger(request_id=request_id)

        self._log_request(logger=logger, request=request, client_ip=client_ip, body_json=body_json)

        try:
            response = await call_next(request)
            duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
            self._log_response(logger, response, duration_ms, request_id)
            return response
        except Exception as e:
            duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
            self._log_error(logger, duration_ms)
            raise

    def _get_or_create_request_id(self, request: Request) -> str:
        return request.headers.get("X-Request-ID") or str(uuid.uuid4())


    def _get_client_ip(self, request: Request) -> str | None:
        client_ip = request.client.host if request.client else None
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            client_ip = forwarded_for.split(",")[0].strip()
        return client_ip


    async def _read_body_safely(self, request: Request):
        body_bytes = await request.body()
        body: str = body_bytes.decode()
        body_json = json.loads(body) 
        request._body = body_bytes
        return body_json

    def _log_request(self, logger, request: Request, client_ip, body_json) -> None:
        logger.info(
            msg="HTTP Request",
            method=request.method,
            url=str(request.url),
            query_params=dict(request.query_params),
            path_params=dict(request.path_params),
            headers=dict(request.headers),
            client_ip=client_ip,
            user_agent=request.headers.get("user-agent"),
            body=body_json,
        )

    def _log_response(self, logger, response: Response, duration_ms, request_id) -> None:
        response.headers["X-Request-ID"] = request_id
        logger.info(
            msg="HTTP Response",
            status_code=response.status_code,
            duration_ms=duration_ms
        )

    def _log_error(self, logger, duration_ms) -> None:
        logger.exception(
            "Request failed",
            status_code=500,
            duration_ms=duration_ms
        )