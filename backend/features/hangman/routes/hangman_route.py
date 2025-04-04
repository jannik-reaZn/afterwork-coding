from typing import Callable

from fastapi import APIRouter, Body, Depends, Query, status

from backend.common.route.enums.api_routes import ApiRoutes
from backend.common.route.enums.api_tags import ApiTags
from backend.features.hangman.domain.models import (
    LANGUAGE_ALPHABETS,
    HangmanAlphabet,
    HangmanGame,
    HangmanLanguage,
    HangmanSettings,
)
from backend.features.hangman.domain.use_cases import (
    GuessHangmanLetterUseCase,
    StartHangmanGameUseCase,
)
from backend.features.hangman.domain.word_provider import get_word_provider_factory
from backend.features.hangman.domain.word_provider.interface import WordProviderInterface
from backend.features.hangman.routes.requests import HangmanRequest

router = APIRouter(prefix=f"/{ApiRoutes.HANGMAN.value}", tags=[ApiTags.HANGMAN])


@router.get(
    "/settings",
    response_model=HangmanSettings,
    status_code=status.HTTP_200_OK,
    description="Retrieval of Hangman settings",
)
async def get_settings(hangman_settings=Depends(HangmanSettings)) -> dict:
    return hangman_settings.model_dump()


@router.get(
    "/alphabet",
    response_model=HangmanAlphabet,
    status_code=status.HTTP_200_OK,
    description="Retrieval of alphabet based on the language",
)
async def get_alphabet(
    language: HangmanLanguage = Query(..., description="Language for alphabet")
) -> HangmanAlphabet:
    return HangmanAlphabet(alphabet=LANGUAGE_ALPHABETS[language])


@router.get(
    "/start",
    response_model=HangmanGame,
    status_code=status.HTTP_200_OK,
    description="Start a new game of Hangman",
)
async def start_hangman(
    tries: int = Query(...),
    language: HangmanLanguage = Query(...),
    word_provider_factory: Callable[[str], WordProviderInterface] = Depends(
        get_word_provider_factory
    ),
) -> HangmanGame:
    return StartHangmanGameUseCase(word_provider_factory)(total_tries=tries, language=language)


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
