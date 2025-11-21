<!-- frontend/src/views/SplashView.vue -->
<template>
  <div class="splash">
    <div class="card">
      <h2>Welcome to D33tcode</h2>
      <p class="subtitle">Sign in to view projects.</p>

      <form @submit.prevent="onSubmit">
        <label>
          Username
          <input v-model="username" autocomplete="username" />
        </label>

        <label>
          Password
          <input
            v-model="password"
            type="password"
            autocomplete="current-password"
          />
        </label>

        <button type="submit" :disabled="loading">
          {{ loading ? "Signing in..." : "Login" }}
        </button>

        <p v-if="error" class="error">{{ error }}</p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { setAuth } from "../stores/auth";

const router = useRouter();

const username = ref("");
const password = ref("");
const loading = ref(false);
const error = ref("");

async function onSubmit() {
  error.value = "";
  loading.value = true;

  try {
    const body = new URLSearchParams();
    body.append("username", username.value);
    body.append("password", password.value);

    const res = await fetch("http://127.0.0.1:8000/api/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body,
    });

    if (!res.ok) {
      const data = await res.json().catch(() => ({}));
      throw new Error(data.detail || "Login failed");
    }

    const data = await res.json();
    // matches TokenResponse from backend
    setAuth({
      token: data.access_token,
      role: data.role,
      username: data.username,
    });

    // route based on role
    if (data.role === "admin") {
      router.push({ name: "admin" });
    } else {
      router.push({ name: "projects" });
    }
  } catch (e) {
    error.value = e.message || "Login failed";
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.splash {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: calc(100vh - 60px);
}
.card {
  width: 100%;
  max-width: 320px;
  padding: 1.5rem;
  border-radius: 0.75rem;
  border: 1px solid #ddd;
  box-shadow: 0 8px 18px rgba(0, 0, 0, 0.05);
  background: #fff;
}
.subtitle {
  color: #555;
  margin-bottom: 1rem;
}
form {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}
label {
  display: flex;
  flex-direction: column;
  font-size: 0.875rem;
}
input {
  margin-top: 0.25rem;
  padding: 0.4rem 0.5rem;
  border: 1px solid #ccc;
  border-radius: 0.4rem;
}
button {
  margin-top: 0.5rem;
  padding: 0.5rem 0.75rem;
  border: none;
  border-radius: 0.4rem;
  background: #2563eb;
  color: white;
  font-weight: 600;
}
button:disabled {
  opacity: 0.6;
}
.error {
  margin-top: 0.5rem;
  color: #b91c1c;
  font-size: 0.85rem;
}
</style>
