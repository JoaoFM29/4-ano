import json
import asyncio


class Tracer:


    def __init__(self) -> None:
        self.lock = asyncio.Lock()
        self.trace = dict()


    async def register(self, project: str) -> None:
        async with self.lock:
            self.trace[project] = True
            await asyncio.sleep(0.001)


    async def deregister(self, project: str) -> None:
        async with self.lock:
            if project in self.trace:
                del self.trace[project]
            await asyncio.sleep(0.001)


    async def cancel(self, project: str) -> None:
        async with self.lock:
            self.trace[project] = False
            await asyncio.sleep(0.001)


    async def getState(self, project: str) -> bool:
        async with self.lock:
            await asyncio.sleep(0.001)
            return self.trace[project]


    def __str__(self) -> str:
        return json.dumps(self.trace, indent=2)