import { reactive } from "vue";

const savedToken = localStorage.getItem("auth_token");
const savedRole = localStorage.getItem("auth_role");
const savedUsername = localStorage.getItem("auth_username");

export const authState = reactive({
  token: savedToken || null,
  role: savedRole || null,
  username: savedUsername || null,
});

export function setAuth({ token, role, username }) {
  authState.token = token;
  authState.role = role;
  authState.username = username;

  localStorage.setItem("auth_token", token);
  localStorage.setItem("auth_role", role);
  localStorage.setItem("auth_username", username);
}

export function clearAuth() {
  authState.token = null;
  authState.role = null;
  authState.username = null;

  localStorage.removeItem("auth_token");
  localStorage.removeItem("auth_role");
  localStorage.removeItem("auth_username");
}
