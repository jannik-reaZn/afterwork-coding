from fastapi import APIRouter, Body, Depends, Query, status

from backend.common.route.enums.api_routes import ApiRoutes
from backend.common.route.enums.api_tags import ApiTags
from backend.features.hangman.domain.models import HangmanStatus
from backend.features.hangman.domain.services import HangmanService, get_hangman_service
from backend.features.hangman.routes.requests import HangmanRequest

router = APIRouter(prefix=f"/{ApiRoutes.HANGMAN.value}", tags=[ApiTags.HANGMAN])


@router.get(
    "/start",
    response_model=HangmanStatus,
    status_code=status.HTTP_200_OK,
    description="Start a new game of Hangman",
)
async def start_hangman(
    tries: int = Query(...),
    language: str = Query(...),
    hangman_service: HangmanService = Depends(get_hangman_service),
) -> HangmanStatus:
    return hangman_service.start_game()


@router.post(
    "/guess/{letter}",
    response_model=HangmanStatus,
    status_code=status.HTTP_200_OK,
    description="Make a guess in the current game of Hangman",
)
async def guess_letter(
    letter: str,
    hangman_request: HangmanRequest = Body(...),
    hangman_service: HangmanService = Depends(get_hangman_service),
) -> HangmanStatus:
    return hangman_service.guess_letter(
        hangman_status=hangman_request, guessed_letter=letter.lower()
    )
