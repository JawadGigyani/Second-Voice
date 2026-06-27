export interface Tile {
  id: number;
  label: string;
  symbol: string;
  category_id: number;
  use_count: number;
  is_quick: boolean;
}

export interface Category {
  id: number;
  name: string;
  icon: string;
  sort_order: number;
}

export interface BoardResponse {
  categories: Category[];
  tiles: Tile[];
}

export interface ComposeResponse {
  text: string;
  source: "gemini" | "fallback";
}
