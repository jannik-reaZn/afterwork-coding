export interface HangmanSettings {
  tries: number[];
  languages: string[];
  modes: string[];
}

export type LanguageKeys = HangmanSettings["languages"][number];
