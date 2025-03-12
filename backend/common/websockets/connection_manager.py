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

    async def connect(self, websocket: WebSocket):
        """
        Accepts a new WebSocket connection and adds it to the list of active connections.

        Args:
            websocket (WebSocket): The WebSocket connection to be accepted and added.
        """
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        """
        Disconnects a given websocket from the active connections.

        Args:
            websocket (WebSocket): The websocket to be disconnected.
        """
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        """
        Sends a personal message to a specific WebSocket connection.

        Args:
            message (str): The message to be sent.
            websocket (WebSocket): The WebSocket connection to which the message will be sent.

        Returns:
            None
        """
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        """
        Broadcasts a message to all active connections.

        Args:
            message (str): The message to be sent to all active connections.
        """
        for connection in self.active_connections:
            await connection.send_text(message)
