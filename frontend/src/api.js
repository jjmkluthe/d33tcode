// frontend/src/api.js
import { authState } from "./stores/auth";

const API_BASE = "http://127.0.0.1:8000/api";

export async function apiGet(path) {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: {
      Authorization: `Bearer ${authState.token}`,
    },
  });
  if (!res.ok) {
    throw new Error(`API error: ${res.status}`);
  }
  return await res.json();
}
