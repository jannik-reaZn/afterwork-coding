from typing import Any, Callable

from fastapi import APIRouter, Body, Depends, Query, status

from backend.common.route.enums.api_routes import ApiRoutes
from backend.common.route.enums.api_tags import ApiTags
from backend.features.hangman.domain.content_factory import get_text_content_factory
from backend.features.hangman.domain.content_factory.interface import ContentFactoryInterface
from backend.features.hangman.domain.models import (
    LANGUAGE_ALPHABETS,
    LANGUAGE_KEYBOARD_LAYOUTS,
    HangmanAlphabet,
    HangmanGame,
    HangmanLanguage,
    HangmanMode,
    HangmanSettings,
)
from backend.features.hangman.domain.use_cases import (
    GuessHangmanLetterUseCase,
    StartHangmanGameUseCase,
)
from backend.features.hangman.routes.requests import HangmanRequest

router = APIRouter(prefix=f"/{ApiRoutes.HANGMAN.value}", tags=[ApiTags.HANGMAN])


@router.get(
    "/settings",
    response_model=HangmanSettings,
    status_code=status.HTTP_200_OK,
    description="Retrieval of Hangman settings",
)
async def get_settings(
    hangman_settings: HangmanSettings = Depends(HangmanSettings),
) -> dict[str, Any]:
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
    return HangmanAlphabet(
        alphabet=LANGUAGE_ALPHABETS[language], layout_hints=LANGUAGE_KEYBOARD_LAYOUTS[language]
    )


@router.get(
    "/start",
    response_model=HangmanGame,
    status_code=status.HTTP_200_OK,
    description="Start a new game of Hangman",
)
async def start_hangman(
    tries: int = Query(...),
    language: HangmanLanguage = Query(...),
    mode: HangmanMode = Query(...),
    content_factory: Callable[[HangmanLanguage, HangmanMode], ContentFactoryInterface] = Depends(
        get_text_content_factory
    ),
) -> HangmanGame:
    return StartHangmanGameUseCase(content_factory)(total_tries=tries, language=language, mode=mode)


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
    hangman_game = HangmanGame(**hangman_request.model_dump())
    return GuessHangmanLetterUseCase()(hangman_status=hangman_game, guessed_letter=letter)
