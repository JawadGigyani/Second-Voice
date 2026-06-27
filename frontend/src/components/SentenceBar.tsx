import type { Tile } from "../types";

interface Props {
  sentence: Tile[];
  composed: string | null;
  onBackspace: () => void;
  onClear: () => void;
}

export default function SentenceBar({
  sentence,
  composed,
  onBackspace,
  onClear,
}: Props) {
  return (
    <div
      data-testid="sentence-bar"
      className="rounded-2xl border border-slate-200 bg-white p-3 dark:border-slate-700 dark:bg-slate-800"
    >
      <div className="min-h-[56px] flex flex-wrap items-center gap-2">
        {sentence.length === 0 && !composed && (
          <span className="text-slate-400 text-tile">
            Tap tiles to build a sentence...
          </span>
        )}
        {composed ? (
          <span className="text-2xl font-semibold text-slate-900 dark:text-slate-50">
            {composed}
          </span>
        ) : (
          sentence.map((t, i) => (
            <span
              key={`${t.id}-${i}`}
              className="flex items-center gap-1 rounded-full bg-sky-100 px-3 py-1 text-tile font-medium text-sky-900 dark:bg-sky-900 dark:text-sky-100"
            >
              <span aria-hidden>{t.symbol}</span>
              {t.label}
            </span>
          ))
        )}
      </div>
      <div className="mt-2 flex justify-end gap-2">
        <button
          type="button"
          onClick={onBackspace}
          className="rounded-xl border border-slate-300 px-4 py-2 font-semibold text-slate-700 hover:bg-slate-100 dark:border-slate-600 dark:text-slate-200 dark:hover:bg-slate-700"
        >
          ⌫ Back
        </button>
        <button
          type="button"
          onClick={onClear}
          className="rounded-xl border border-slate-300 px-4 py-2 font-semibold text-slate-700 hover:bg-slate-100 dark:border-slate-600 dark:text-slate-200 dark:hover:bg-slate-700"
        >
          Clear
        </button>
      </div>
    </div>
  );
}
