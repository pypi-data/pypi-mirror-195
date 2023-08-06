# !/usr/bin/python

import asyncio

from tapp import TApp

app = TApp()


@app.route(method="method")
async def method_handler(message: str, version: str) -> None:
    print(message, version)


@app.on_lifespan("startup")
async def startup() -> None:
    print("startup")


@app.on_lifespan("shutdown")
async def on_shutdown() -> None:
    print("shutdown")


async def main() -> None:
    await app("lifespan")

    await app(
        method="method",
        original_update={
            "method": "method",
            "event": "message"
        },
        event="message",
        version="version"
    )

    await app("lifespan")


if __name__ == "__main__":
    asyncio.run(main())
