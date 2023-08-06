from typing import Any, Callable, Coroutine, Dict, Optional, Sequence, Type

from .filters import Filter
from .middleware import BaseMiddleware
from .routing import TRoute, TRouter
from .types import Decorated


class TApp:
    def __init__(
        self,
        router_class: Type[TRouter] = TRouter,
        *,
        routes: Optional[Sequence[TRoute]] = None,
        on_startup: Optional[Sequence[Callable[..., Any]]] = None,
        on_shutdown: Optional[Sequence[Callable[..., Any]]] = None,
        middleware: Optional[Sequence[BaseMiddleware]] = None,
        outer_middleware: Optional[Sequence[BaseMiddleware]] = None,
        exception_handlers: Optional[
            Dict[
                Type[Exception],
                Callable[[Any, Exception], Coroutine[Any, Any, Any]],
            ]
        ] = None,
    ) -> None:
        self.router = router_class(
            routes=routes,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            middleware=middleware,
            outer_middleware=outer_middleware,
            exception_handlers=exception_handlers,
        )

    async def __call__(
        self,
        method: str,
        original_update: Optional[Any] = None,
        event: Optional[Any] = None,
        **kwargs: Any,
    ) -> None:
        if method == "lifespan":
            await self.router.lifespan()
            return

        kwargs["original_update"] = original_update

        async def wrap(update: Any, **data: Any) -> None:
            await self.router(method=method, update=update, **data)

        wrapped = self.router.outer_middleware.wrap(wrap)
        await wrapped(event, kwargs)

    def include_router(self, router: TRouter) -> None:
        self.router.include_router(router)

    def add_middleware(self, middleware: BaseMiddleware) -> None:
        self.router.add_middleware(middleware)

    def add_outer_middleware(self, outer_middleware: BaseMiddleware) -> None:
        self.router.add_outer_middleware(outer_middleware)

    def add_route(
        self,
        endpoint: Callable[..., Any],
        *,
        method: str,
        filters: Optional[Sequence[Filter]] = None,
        flags: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.router.add_route(endpoint=endpoint, method=method, filters=filters, flags=flags)

    def route(
        self,
        *filters: Filter,
        method: str,
        flags: Optional[Dict[str, Any]] = None,
    ) -> Callable[[Decorated], Decorated]:
        return self.router.route(*filters, method=method, flags=flags)

    def add_lifespan(
        self,
        method: str,
        endpoint: Callable[..., Any],
    ) -> None:
        self.router.add_lifespan(method=method, endpoint=endpoint)

    def on_lifespan(self, method: str) -> Callable[[Decorated], Decorated]:
        return self.router.on_lifespan(method=method)

    def add_exception_handler(
        self,
        exception: Type[Exception],
        endpoint: Callable[..., Any],
    ) -> None:
        self.router.add_exception_handler(exception=exception, endpoint=endpoint)

    def exception_handler(self, exception: Type[Exception]) -> Callable[[Decorated], Decorated]:
        return self.router.exception_handler(exception=exception)
