import type { Tile as TileType } from "../types";

interface Props {
  tile: TileType;
  scanActive?: boolean;
  onSelect: (t: TileType) => void;
}

export default function Tile({ tile, scanActive, onSelect }: Props) {
  return (
    <button
      type="button"
      aria-label={tile.label}
      onClick={() => onSelect(tile)}
      className={[
        "flex flex-col items-center justify-center gap-1 rounded-2xl p-3",
        "min-h-[96px] select-none border shadow-sm transition active:scale-95",
        "bg-white text-slate-900 border-slate-200",
        "dark:bg-slate-800 dark:text-slate-50 dark:border-slate-700",
        "hover:border-sky-400 focus:outline-none focus-visible:ring-4 focus-visible:ring-sky-400",
        scanActive ? "scan-active" : "",
      ].join(" ")}
    >
      <span className="text-4xl leading-none" aria-hidden>
        {tile.symbol}
      </span>
      <span className="text-tile font-semibold text-center leading-tight">
        {tile.label}
      </span>
    </button>
  );
}
