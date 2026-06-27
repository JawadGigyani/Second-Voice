import { create } from "zustand";
import { persist } from "zustand/middleware";
import type { Tile } from "./types";

export interface Settings {
  highContrast: boolean;
  textScale: number; // 1 = normal
  voice: string;
  speed: number;
  scanning: boolean;
  scanIntervalMs: number;
}

interface AppState {
  sentence: Tile[];
  composed: string | null;
  settings: Settings;
  addTile: (t: Tile) => void;
  backspace: () => void;
  clear: () => void;
  setComposed: (text: string | null) => void;
  updateSettings: (patch: Partial<Settings>) => void;
}

const defaultSettings: Settings = {
  highContrast: false,
  textScale: 1,
  voice: "af_heart",
  speed: 1.0,
  scanning: false,
  scanIntervalMs: 1200,
};

export const useStore = create<AppState>()(
  persist(
    (set) => ({
      sentence: [],
      composed: null,
      settings: defaultSettings,
      addTile: (t) =>
        set((s) => ({ sentence: [...s.sentence, t], composed: null })),
      backspace: () =>
        set((s) => ({ sentence: s.sentence.slice(0, -1), composed: null })),
      clear: () => set({ sentence: [], composed: null }),
      setComposed: (text) => set({ composed: text }),
      updateSettings: (patch) =>
        set((s) => ({ settings: { ...s.settings, ...patch } })),
    }),
    {
      name: "second-voice",
      partialize: (s) => ({ settings: s.settings }),
    },
  ),
);
