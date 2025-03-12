from collections import defaultdict

from fastapi import WebSocket


class ConnectionManager:
    """
    Manages WebSocket connections and provides methods to handle connection events and message
    broadcasting.

    The implementation is based on the FastAPI WebSocket example:
    https://fastapi.tiangolo.com/advanced/websockets/
    """

    def __init__(self):
        self.active_connections: list[WebSocket] = []
        self.channels: dict[str, set[WebSocket]] = defaultdict(set)

    async def connect(self, websocket: WebSocket):
        """Accepts a new WebSocket connection and adds it to the list of active connections."""
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        """Removes a WebSocket connection from active connections and all subscribed channels."""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

        for channel in self.channels.values():
            channel.discard(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket) -> None:
        """Sends a personal message to a specific WebSocket connection."""
        await websocket.send_text(message)

    async def broadcast(self, message: str) -> None:
        """Broadcasts a message to all active connections."""
        for connection in self.active_connections:
            await connection.send_text(message)

    def subscribe(self, websocket: WebSocket, channel: str) -> None:
        """Subscribes a WebSocket connection to a specific channel."""
        self.channels[channel].add(websocket)

    def unsubscribe(self, websocket: WebSocket, channel: str) -> None:
        """Unsubscribes a WebSocket connection from a specific channel."""
        if channel in self.channels:
            self.channels[channel].discard(websocket)
            if not self.channels[channel]:  # Cleanup empty channels
                del self.channels[channel]

    async def send_to_channel(self, message: str, channel: str) -> None:
        """Sends a message to all subscribers of a specific channel."""
        if channel in self.channels:
            for connection in self.channels[channel]:
                await connection.send_text(message)
