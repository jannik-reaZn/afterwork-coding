export interface HangmanSettings {
  tries: number[];
  languages: string[];
}

export type LanguageKeys = HangmanSettings["languages"][number];
