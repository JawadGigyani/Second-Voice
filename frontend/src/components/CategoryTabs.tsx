import type { Category } from "../types";

interface Props {
  categories: Category[];
  active: number | null;
  onChange: (id: number) => void;
}

export default function CategoryTabs({ categories, active, onChange }: Props) {
  return (
    <div
      className="flex gap-2 overflow-x-auto pb-1"
      role="tablist"
      aria-label="Categories"
    >
      {categories.map((c) => {
        const selected = c.id === active;
        return (
          <button
            key={c.id}
            role="tab"
            aria-selected={selected}
            onClick={() => onChange(c.id)}
            className={[
              "flex shrink-0 items-center gap-2 rounded-full px-4 py-2 text-tile font-semibold",
              "border transition focus:outline-none focus-visible:ring-4 focus-visible:ring-sky-400",
              selected
                ? "bg-sky-600 text-white border-sky-600"
                : "bg-white text-slate-700 border-slate-200 dark:bg-slate-800 dark:text-slate-200 dark:border-slate-700",
            ].join(" ")}
          >
            <span aria-hidden className="text-xl">
              {c.icon}
            </span>
            {c.name}
          </button>
        );
      })}
    </div>
  );
}
