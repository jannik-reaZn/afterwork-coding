import axiosInstance from "./axiosInstance";
import { HangmanGame } from "@/models/hangmanModel";

export async function startHangmanGame(
  tries: number,
  language: string
): Promise<HangmanGame> {
  const path = "/hangman/start";
  const params = {
    tries,
    language,
  };
  try {
    const response = await axiosInstance.get(path, { params });
    return response.data;
  } catch (error: any) {
    throw error;
  }
}

export async function guessLetterHangmanGame(
  guessedLetter: string,
  gameState: HangmanGame
): Promise<HangmanGame> {
  const path = `/hangman/guess/${guessedLetter}`;
  try {
    const response = await axiosInstance.post(path, gameState);
    return response.data;
  } catch (error: any) {
    throw error;
  }
}
