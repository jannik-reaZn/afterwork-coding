from unittest.mock import AsyncMock

import pytest
from fastapi.websockets import WebSocket

from backend.common.websockets import ConnectionManager


@pytest.fixture
def connection_manager() -> ConnectionManager:
    """Fixture to provide a fresh instance of ConnectionManager for each test."""
    return ConnectionManager()


@pytest.fixture
def mock_websocket() -> AsyncMock:
    """Fixture to provide a mock WebSocket connection."""
    return AsyncMock(spec=WebSocket)


@pytest.mark.asyncio
async def test_connect(connection_manager, mock_websocket):
    await connection_manager.connect(mock_websocket)

    assert mock_websocket in connection_manager.active_connections
    mock_websocket.accept.assert_awaited_once()


@pytest.mark.asyncio
async def test_disconnect(connection_manager, mock_websocket):
    await connection_manager.connect(mock_websocket)
    connection_manager.disconnect(mock_websocket)

    assert mock_websocket not in connection_manager.active_connections


@pytest.mark.asyncio
async def test_subscribe_and_unsubscribe(connection_manager, mock_websocket):
    channel = "game_room_1"

    await connection_manager.connect(mock_websocket)
    connection_manager.subscribe(mock_websocket, channel)

    assert mock_websocket in connection_manager.channels[channel]

    connection_manager.unsubscribe(mock_websocket, channel)

    assert mock_websocket not in connection_manager.channels[channel]
    assert not connection_manager.channels[channel]


@pytest.mark.asyncio
async def test_send_personal_message(connection_manager, mock_websocket):
    await connection_manager.connect(mock_websocket)
    message = "Hello, player!"

    await connection_manager.send_personal_message(message, mock_websocket)

    mock_websocket.send_text.assert_awaited_once_with(message)


@pytest.mark.asyncio
async def test_broadcast(connection_manager):
    mock_websocket1 = AsyncMock(spec=WebSocket)
    mock_websocket2 = AsyncMock(spec=WebSocket)

    await connection_manager.connect(mock_websocket1)
    await connection_manager.connect(mock_websocket2)

    message = "Game update!"
    await connection_manager.broadcast(message)

    mock_websocket1.send_text.assert_awaited_once_with(message)
    mock_websocket2.send_text.assert_awaited_once_with(message)


@pytest.mark.asyncio
async def test_send_to_channel(connection_manager):
    mock_websocket1 = AsyncMock(spec=WebSocket)
    mock_websocket2 = AsyncMock(spec=WebSocket)
    mock_websocket3 = AsyncMock(spec=WebSocket)  # Not subscribed

    await connection_manager.connect(mock_websocket1)
    await connection_manager.connect(mock_websocket2)
    await connection_manager.connect(mock_websocket3)

    channel = "room1"
    connection_manager.subscribe(mock_websocket1, channel)
    connection_manager.subscribe(mock_websocket2, channel)

    message = "Channel message"
    await connection_manager.send_to_channel(message, channel)

    mock_websocket1.send_text.assert_awaited_once_with(message)
    mock_websocket2.send_text.assert_awaited_once_with(message)
    mock_websocket3.send_text.assert_not_awaited()  # Should not receive the message
