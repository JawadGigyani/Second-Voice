import type { BoardResponse, ComposeResponse } from "./types";

const BASE = import.meta.env.VITE_API_BASE ?? "";

async function jsonFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...init,
  });
  if (!res.ok) {
    const detail = await res.text().catch(() => "");
    throw new Error(`${res.status} ${res.statusText} ${detail}`);
  }
  return res.json() as Promise<T>;
}

export async function getBoard(): Promise<BoardResponse> {
  return jsonFetch<BoardResponse>("/api/board");
}

export async function markTileUsed(id: number): Promise<void> {
  // Fire-and-forget; ignore failures so the UI never blocks.
  try {
    await fetch(`${BASE}/api/tiles/${id}/use`, { method: "POST" });
  } catch {
    /* noop */
  }
}

export async function compose(tiles: string[]): Promise<ComposeResponse> {
  return jsonFetch<ComposeResponse>("/api/compose", {
    method: "POST",
    body: JSON.stringify({ tiles }),
  });
}

export async function speak(
  text: string,
  voice?: string,
  speed?: number,
): Promise<Blob> {
  const res = await fetch(`${BASE}/api/speak`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text, voice, speed }),
  });
  if (!res.ok) {
    const detail = await res.text().catch(() => "");
    throw new Error(`speak failed: ${res.status} ${detail}`);
  }
  return res.blob();
}
