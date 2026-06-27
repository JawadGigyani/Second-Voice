import { useStore } from "../store";

const VOICES = [
  "af_heart",
  "af_bella",
  "af_nicole",
  "af_sarah",
  "am_adam",
  "am_michael",
  "bf_emma",
  "bm_george",
];

interface Props {
  open: boolean;
  onClose: () => void;
}

export default function SettingsPanel({ open, onClose }: Props) {
  const { settings, updateSettings } = useStore();
  if (!open) return null;
  return (
    <div
      className="fixed inset-0 z-40 flex justify-end bg-black/40"
      onClick={onClose}
    >
      <div
        className="h-full w-full max-w-sm overflow-y-auto bg-white p-5 dark:bg-slate-900"
        onClick={(e) => e.stopPropagation()}
        role="dialog"
        aria-label="Settings"
      >
        <div className="mb-4 flex items-center justify-between">
          <h2 className="text-xl font-bold dark:text-white">Settings</h2>
          <button
            onClick={onClose}
            className="rounded-lg px-3 py-1 text-lg font-bold text-slate-500 hover:bg-slate-100 dark:hover:bg-slate-800"
            aria-label="Close settings"
          >
            ✕
          </button>
        </div>

        <label className="mb-4 flex items-center justify-between">
          <span className="font-semibold dark:text-slate-100">
            High contrast
          </span>
          <input
            type="checkbox"
            className="h-6 w-6"
            checked={settings.highContrast}
            onChange={(e) => updateSettings({ highContrast: e.target.checked })}
          />
        </label>

        <div className="mb-4">
          <label className="font-semibold dark:text-slate-100">
            Text size: {Math.round(settings.textScale * 100)}%
          </label>
          <input
            type="range"
            min={0.8}
            max={2}
            step={0.1}
            value={settings.textScale}
            onChange={(e) =>
              updateSettings({ textScale: Number(e.target.value) })
            }
            className="w-full"
          />
        </div>

        <div className="mb-4">
          <label className="font-semibold dark:text-slate-100">Voice</label>
          <select
            value={settings.voice}
            onChange={(e) => updateSettings({ voice: e.target.value })}
            className="mt-1 w-full rounded-lg border border-slate-300 p-2 dark:bg-slate-800 dark:text-white"
          >
            {VOICES.map((v) => (
              <option key={v} value={v}>
                {v}
              </option>
            ))}
          </select>
        </div>

        <div className="mb-4">
          <label className="font-semibold dark:text-slate-100">
            Speed: {settings.speed.toFixed(1)}x
          </label>
          <input
            type="range"
            min={0.6}
            max={1.6}
            step={0.1}
            value={settings.speed}
            onChange={(e) => updateSettings({ speed: Number(e.target.value) })}
            className="w-full"
          />
        </div>

        <label className="mb-4 flex items-center justify-between">
          <span className="font-semibold dark:text-slate-100">
            Scanning mode (switch access)
          </span>
          <input
            type="checkbox"
            className="h-6 w-6"
            checked={settings.scanning}
            onChange={(e) => updateSettings({ scanning: e.target.checked })}
          />
        </label>

        {settings.scanning && (
          <div className="mb-4">
            <label className="font-semibold dark:text-slate-100">
              Scan speed: {(settings.scanIntervalMs / 1000).toFixed(1)}s
            </label>
            <input
              type="range"
              min={600}
              max={3000}
              step={100}
              value={settings.scanIntervalMs}
              onChange={(e) =>
                updateSettings({ scanIntervalMs: Number(e.target.value) })
              }
              className="w-full"
            />
            <p className="mt-1 text-sm text-slate-500">
              Press Space or tap the screen to select the highlighted item.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
