from fastapi import APIRouter, Body, Query, status

from backend.common.route.enums.api_routes import ApiRoutes
from backend.common.route.enums.api_tags import ApiTags
from backend.features.hangman.domain.models import HangmanGame
from backend.features.hangman.domain.use_cases import (
    GuessHangmanLetterUseCase,
    StartHangmanGameUseCase,
)
from backend.features.hangman.domain.word_provider import get_word_provider_factory
from backend.features.hangman.routes.requests import HangmanRequest

router = APIRouter(prefix=f"/{ApiRoutes.HANGMAN.value}", tags=[ApiTags.HANGMAN])


@router.get(
    "/start",
    response_model=HangmanGame,
    status_code=status.HTTP_200_OK,
    description="Start a new game of Hangman",
)
async def start_hangman(
    tries: int = Query(...),
    language: str = Query(...),
) -> HangmanGame:
    return StartHangmanGameUseCase(get_word_provider_factory())(
        total_tries=tries, language=language
    )


@router.post(
    "/guess/{letter}",
    response_model=HangmanGame,
    status_code=status.HTTP_200_OK,
    description="Make a guess in the current game of Hangman",
)
async def guess_letter(
    letter: str,
    hangman_request: HangmanRequest = Body(...),
) -> HangmanGame:
    return GuessHangmanLetterUseCase()(hangman_status=hangman_request, guessed_letter=letter)
