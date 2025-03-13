import axiosInstance from "./axiosInstance";
import { HangmanGame } from "@/models/hangmanModel";

export async function startHangmanGame(): Promise<HangmanGame> {
  const path = "/hangman/start";
  try {
    const response = await axiosInstance.get(path);
    return response.data;
  } catch (error: any) {
    throw error;
  }
}

export async function updateHangmanGame(payload: {
  gameId: string;
  guessedLetter: string;
}): Promise<{}> {
  const path = "/hangman/update";
  try {
    const response = await axiosInstance.post(path, payload);
    return response.data;
  } catch (error: any) {
    throw error;
  }
}
