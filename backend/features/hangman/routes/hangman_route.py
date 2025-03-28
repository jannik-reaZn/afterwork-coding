from fastapi import APIRouter, Body, Depends, status

from backend.common.route.enums.api_routes import ApiRoutes
from backend.common.route.enums.api_tags import ApiTags
from backend.features.hangman.domain.models import HangmanLanguages, HangmanStatus
from backend.features.hangman.domain.services import HangmanService
from backend.features.hangman.domain.services.word_provider import WordProviderFaker
from backend.features.hangman.routes.requests import HangmanRequest

router = APIRouter(prefix=f"/{ApiRoutes.HANGMAN.value}", tags=[ApiTags.HANGMAN])


def get_hangman_service() -> HangmanService:
    word_provider = WordProviderFaker(language=HangmanLanguages.ENGLISH.value)
    return HangmanService(word_provider=word_provider)


@router.get(
    "/start",
    response_model=HangmanStatus,
    status_code=status.HTTP_200_OK,
    description="Start a new game of Hangman",
)
async def start_hangman(
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
    return hangman_service.guess_letter(hangman_status=hangman_request, guessed_letter=letter)
