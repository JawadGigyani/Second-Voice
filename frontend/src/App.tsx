import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import CategoryTabs from "./components/CategoryTabs";
import SentenceBar from "./components/SentenceBar";
import SettingsPanel from "./components/SettingsPanel";
import TileButton from "./components/Tile";
import { compose, getBoard, markTileUsed, speak } from "./api";
import { useStore } from "./store";
import type { BoardResponse, Tile } from "./types";

export default function App() {
  const [board, setBoard] = useState<BoardResponse | null>(null);
  const [activeCat, setActiveCat] = useState<number | null>(null);
  const [settingsOpen, setSettingsOpen] = useState(false);
  const [status, setStatus] = useState<string>("");
  const [scanIndex, setScanIndex] = useState(0);

  const { sentence, composed, settings, addTile, backspace, clear, setComposed } =
    useStore();
  const audioRef = useRef<HTMLAudioElement | null>(null);

  // Apply theme + text scaling.
  useEffect(() => {
    const root = document.documentElement;
    root.classList.toggle("dark", settings.highContrast);
    root.style.setProperty("--tile-font", `${(1.05 * settings.textScale).toFixed(3)}rem`);
  }, [settings.highContrast, settings.textScale]);

  // Load board.
  useEffect(() => {
    getBoard()
      .then((b) => {
        setBoard(b);
        setActiveCat(b.categories[0]?.id ?? null);
      })
      .catch((e) => setStatus(`Failed to load board: ${e.message}`));
  }, []);

  const tiles = useMemo(
    () => (board ? board.tiles.filter((t) => t.category_id === activeCat) : []),
    [board, activeCat],
  );

  const playBlob = useCallback(async (blob: Blob) => {
    const url = URL.createObjectURL(blob);
    if (!audioRef.current) audioRef.current = new Audio();
    audioRef.current.src = url;
    await audioRef.current.play().catch(() => {});
  }, []);

  const speakText = useCallback(
    async (text: string) => {
      if (!text.trim()) return;
      setStatus("Speaking...");
      try {
        const blob = await speak(text, settings.voice, settings.speed);
        await playBlob(blob);
        setStatus("");
      } catch (e) {
        setStatus(`Speech unavailable: ${(e as Error).message}`);
      }
    },
    [settings.voice, settings.speed, playBlob],
  );

  const onSelectTile = useCallback(
    (t: Tile) => {
      markTileUsed(t.id);
      if (t.is_quick) {
        // Quick replies are complete phrases: speak immediately.
        speakText(t.label);
        return;
      }
      addTile(t);
    },
    [addTile, speakText],
  );

  const handleSpeak = useCallback(async () => {
    if (composed) {
      await speakText(composed);
      return;
    }
    if (sentence.length === 0) return;
    setStatus("Composing...");
    let text = sentence.map((t) => t.label).join(" ");
    try {
      const r = await compose(sentence.map((t) => t.label));
      if (r.text) text = r.text;
    } catch {
      /* fall back to joined labels */
    }
    setComposed(text);
    await speakText(text);
  }, [composed, sentence, setComposed, speakText]);

  // Scanning mode: cycle highlight over [Speak, ...tiles]; Space selects.
  const scanCount = tiles.length + 1;
  useEffect(() => {
    if (!settings.scanning) return;
    const id = window.setInterval(() => {
      setScanIndex((i) => (i + 1) % scanCount);
    }, settings.scanIntervalMs);
    return () => window.clearInterval(id);
  }, [settings.scanning, settings.scanIntervalMs, scanCount]);

  useEffect(() => {
    if (!settings.scanning) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.code === "Space" || e.code === "Enter") {
        e.preventDefault();
        if (scanIndex === 0) handleSpeak();
        else onSelectTile(tiles[scanIndex - 1]);
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [settings.scanning, scanIndex, tiles, handleSpeak, onSelectTile]);

  return (
    <div className="min-h-full bg-slate-100 text-slate-900 dark:bg-slate-950 dark:text-slate-50">
      <div className="mx-auto flex min-h-screen max-w-4xl flex-col gap-3 p-3">
        <header className="flex items-center justify-between">
          <h1 className="text-2xl font-extrabold tracking-tight">
            🗣️ Second Voice
          </h1>
          <button
            onClick={() => setSettingsOpen(true)}
            aria-label="Open settings"
            className="rounded-xl border border-slate-300 px-4 py-2 font-semibold hover:bg-white dark:border-slate-700 dark:hover:bg-slate-800"
          >
            ⚙️ Settings
          </button>
        </header>

        <SentenceBar
          sentence={sentence}
          composed={composed}
          onBackspace={backspace}
          onClear={clear}
        />

        <button
          type="button"
          onClick={handleSpeak}
          className={[
            "rounded-2xl bg-emerald-600 py-5 text-2xl font-extrabold text-white shadow-lg",
            "transition active:scale-[0.98] hover:bg-emerald-500",
            "focus:outline-none focus-visible:ring-4 focus-visible:ring-emerald-300",
            settings.scanning && scanIndex === 0 ? "scan-active" : "",
          ].join(" ")}
        >
          🔊 Speak
        </button>

        {status && (
          <div className="text-center text-sm text-slate-500" role="status">
            {status}
          </div>
        )}

        {board && (
          <CategoryTabs
            categories={board.categories}
            active={activeCat}
            onChange={(id) => {
              setActiveCat(id);
              setScanIndex(0);
            }}
          />
        )}

        <main className="grid grid-cols-3 gap-3 sm:grid-cols-4 md:grid-cols-5">
          {tiles.map((t, i) => (
            <TileButton
              key={t.id}
              tile={t}
              scanActive={settings.scanning && scanIndex === i + 1}
              onSelect={onSelectTile}
            />
          ))}
        </main>

        <footer className="mt-auto pt-2 text-center text-xs text-slate-400">
          Built free with kokoro-onnx + Gemini · Track 03
        </footer>
      </div>

      <SettingsPanel open={settingsOpen} onClose={() => setSettingsOpen(false)} />
    </div>
  );
}
