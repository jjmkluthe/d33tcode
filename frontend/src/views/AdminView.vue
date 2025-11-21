<template>
  <div class="admin-page">
    <h2>Admin Panel</h2>

    <section class="panel">
      <h3>Users</h3>
      <p v-if="usersLoading">Loading users...</p>
      <p v-if="usersError" class="error">{{ usersError }}</p>

      <table v-if="users.length">
        <thead>
          <tr>
            <th>ID</th>
            <th>Username</th>
            <th>Email</th>
            <th>Role</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="u in users" :key="u.id">
            <td>{{ u.id }}</td>
            <td>{{ u.username }}</td>
            <td>{{ u.email_address }}</td>
            <td>{{ u.role }}</td>
          </tr>
        </tbody>
      </table>
      <p v-else-if="!usersLoading && !usersError">No users found.</p>
    </section>

    <section class="panel">
      <h3>Projects by Difficulty</h3>
      <p v-if="projectsLoading">Loading projects...</p>
      <p v-if="projectsError" class="error">{{ projectsError }}</p>

      <div v-if="!projectsLoading && !projectsError">
        <div class="chart">
          <div
            v-for="d in difficulties"
            :key="d"
            class="bar-row"
          >
            <span class="label">Difficulty {{ d }}</span>
            <div class="bar-wrapper">
              <div
                class="bar"
                :style="{ width: barWidth(d) + '%' }"
              >
                {{ countsByDifficulty[d] || 0 }}
              </div>
            </div>
          </div>
        </div>
        <p class="hint">
          Bars show how many projects have each difficulty level.
        </p>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { authState } from "../stores/auth";

const API_BASE = "http://127.0.0.1:8000/api";

const users = ref([]);
const usersLoading = ref(false);
const usersError = ref("");

const projects = ref([]);
const projectsLoading = ref(false);
const projectsError = ref("");

const difficulties = [1, 2, 3, 4, 5];

function authHeader() {
  return {
    Authorization: `Bearer ${authState.token}`,
  };
}

async function fetchUsers() {
  usersLoading.value = true;
  usersError.value = "";
  try {
    const res = await fetch(`${API_BASE}/users`, {
      headers: {
        ...authHeader(),
        Accept: "application/json",
      },
    });
    if (!res.ok) {
      const data = await res.json().catch(() => ({}));
      throw new Error(data.detail || "Failed to load users");
    }
    users.value = await res.json();
  } catch (e) {
    usersError.value = e.message || "Failed to load users";
  } finally {
    usersLoading.value = false;
  }
}

async function fetchProjects() {
  projectsLoading.value = true;
  projectsError.value = "";
  try {
    const res = await fetch(`${API_BASE}/projects`, {
      headers: {
        ...authHeader(),
        Accept: "application/json",
      },
    });
    if (!res.ok) {
      const data = await res.json().catch(() => ({}));
      throw new Error(data.detail || "Failed to load projects");
    }
    projects.value = await res.json();
  } catch (e) {
    projectsError.value = e.message || "Failed to load projects";
  } finally {
    projectsLoading.value = false;
  }
}

const countsByDifficulty = computed(() => {
  const counts = {};
  for (const d of difficulties) counts[d] = 0;

  for (const p of projects.value) {
    const d = p.difficulty;
    if (d && counts[d] !== undefined) {
      counts[d] += 1;
    }
  }
  return counts;
});

const maxCount = computed(() => {
  const values = Object.values(countsByDifficulty.value);
  return values.length ? Math.max(...values, 1) : 1;
});

function barWidth(difficulty) {
  const count = countsByDifficulty.value[difficulty] || 0;
  if (maxCount.value === 0) return 0;
  return (count / maxCount.value) * 100;
}

onMounted(() => {
  if (authState.token && authState.role === "admin") {
    fetchUsers();
    fetchProjects();
  }
});
</script>

<style scoped>
.admin {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  max-width: 800px;
  margin: 0 auto;
  color: #111827; /* force dark text */
}

.card {
  background: #ffffff;
  border-radius: 0.75rem;
  padding: 1rem 1.25rem 1.25rem;
  box-shadow: 0 8px 18px rgba(15, 23, 42, 0.08);
  border: 1px solid #e5e7eb;
}

.card-title {
  font-size: 1.1rem;
  font-weight: 700;
  margin-bottom: 0.75rem;
  color: #111827;
}

.users-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9rem;
}

.users-table thead {
  background: #f9fafb;
}

.users-table th,
.users-table td {
  padding: 0.4rem 0.5rem;
  text-align: left;
  border-bottom: 1px solid #e5e7eb;
  color: #111827; /* critical: ensure visible text */
}

.users-table th {
  font-weight: 600;
}

.stats-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.stat-row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.stat-label {
  width: 6.5rem;
  font-size: 0.85rem;
  color: #374151;
}

.bar-track {
  position: relative;
  flex: 1;
  height: 0.9rem;
  border-radius: 999px;
  background: #f3f4f6;
  overflow: hidden;
}

.bar-fill {
  position: absolute;
  inset: 0;
  max-width: 100%;
  border-radius: 999px;
  background: #2563eb;
}

.bar-count {
  position: relative;
  z-index: 1;
  font-size: 0.75rem;
  color: #111827;
  padding-left: 0.35rem;
}

.caption {
  margin-top: 0.5rem;
  font-size: 0.8rem;
  color: #4b5563;
}

.muted {
  font-size: 0.85rem;
  color: #6b7280;
}
</style>
