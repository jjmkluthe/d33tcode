<!-- frontend/src/App.vue -->
<template>
  <div class="app">
    <header class="app-header">
      <h1>D33tcode</h1>
      <div v-if="auth.username" class="user-info">
        <span>{{ auth.username }} ({{ auth.role }})</span>
        <button @click="logout">Logout</button>
      </div>
    </header>

    <main class="app-main">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { authState, clearAuth } from "./stores/auth";

const auth = authState;

function logout() {
  clearAuth();
}
</script>

<style scoped>
.app {
  font-family: system-ui, sans-serif;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 1.25rem;
  border-bottom: 1px solid #ddd;
}
.app-main {
  flex: 1;
  padding: 1.5rem;
}
button {
  cursor: pointer;
}
</style>
