<template>
  <div class="projects-page">
    <div class="header-row">
      <h2>Projects</h2>
      <div class="header-actions" v-if="isAdmin">
        <button @click="openNewProject">+ Add Project</button>
      </div>
    </div>

    <p v-if="loading">Loading projects...</p>
    <p v-if="error" class="error">{{ error }}</p>

    <table v-if="!loading && projects.length" class="projects-table">
      <thead>
        <tr>
          <th>Title</th>
          <th>Difficulty</th>
          <th>Description</th>
          <th style="width: 120px;">Action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="proj in projects" :key="proj.id">
          <td>{{ proj.title }}</td>
          <td>{{ proj.difficulty ?? "-" }}</td>
          <td class="description-cell">
            {{ proj.description || "No description" }}
          </td>
          <td class="actions-cell">
            <button
              v-if="isAdmin"
              @click="openEditProject(proj)"
            >
              Edit
            </button>
            <button
              v-else
              @click="onStart(proj)"
            >
              Start
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <p v-if="!loading && !projects.length && !error">
      No projects found.
    </p>

    <!-- Simple modal for create/edit -->
    <div v-if="showModal" class="modal-backdrop" @click.self="closeModal">
      <div class="modal">
        <h3>{{ modalTitle }}</h3>

        <form @submit.prevent="saveProject">
          <label>
            Title
            <input v-model="form.title" required />
          </label>

          <label>
            Description
            <textarea v-model="form.description" rows="3" />
          </label>

          <label>
            Problem ID
            <input
              v-model.number="form.problem_id"
              type="number"
              min="1"
              placeholder="optional"
            />
          </label>

          <label>
            Solution ID
            <input
              v-model.number="form.solution_id"
              type="number"
              min="1"
              placeholder="optional"
            />
          </label>

          <label>
            Difficulty (1–5)
            <input
              v-model.number="form.difficulty"
              type="number"
              min="1"
              max="5"
              placeholder="optional"
            />
          </label>

          <p v-if="modalError" class="error">{{ modalError }}</p>

          <div class="modal-actions">
            <button type="button" @click="closeModal">Cancel</button>
            <button type="submit" :disabled="saving">
              {{ saving ? "Saving..." : "Save" }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, reactive, ref, computed } from "vue";
import { authState } from "../stores/auth";

const API_BASE = "http://127.0.0.1:8000/api";

const projects = ref([]);
const loading = ref(false);
const error = ref("");

const showModal = ref(false);
const saving = ref(false);
const modalError = ref("");
const isNew = ref(true);
const currentId = ref(null);

const form = reactive({
  title: "",
  description: "",
  problem_id: null,
  solution_id: null,
  difficulty: null,
});

const isAdmin = computed(() => authState.role === "admin");

const modalTitle = computed(() =>
  isNew.value ? "Add Project" : "Edit Project"
);

async function fetchProjects() {
  loading.value = true;
  error.value = "";

  try {
    const res = await fetch(`${API_BASE}/projects`, {
      headers: {
        Authorization: `Bearer ${authState.token}`,
        Accept: "application/json",
      },
    });

    if (!res.ok) {
      const data = await res.json().catch(() => ({}));
      throw new Error(data.detail || "Failed to load projects");
    }

    const data = await res.json();
    projects.value = data;
  } catch (e) {
    error.value = e.message || "Failed to load projects";
  } finally {
    loading.value = false;
  }
}

function openNewProject() {
  isNew.value = true;
  currentId.value = null;
  modalError.value = "";
  form.title = "";
  form.description = "";
  form.problem_id = null;
  form.solution_id = null;
  form.difficulty = null;
  showModal.value = true;
}

function openEditProject(proj) {
  isNew.value = false;
  currentId.value = proj.id;
  modalError.value = "";
  form.title = proj.title ?? "";
  form.description = proj.description ?? "";
  form.problem_id = proj.problem_id ?? null;
  form.solution_id = proj.solution_id ?? null;
  form.difficulty = proj.difficulty ?? null;
  showModal.value = true;
}

function closeModal() {
  showModal.value = false;
}

async function saveProject() {
  if (!isAdmin.value) return;

  saving.value = true;
  modalError.value = "";

  // Build payload matching backend ProjectIn
  const payload = {
    title: form.title,
    description: form.description || null,
    problem_id: form.problem_id || null,
    solution_id: form.solution_id || null,
    difficulty: form.difficulty || null,
  };

  try {
    const url = isNew.value
      ? `${API_BASE}/projects`
      : `${API_BASE}/projects/${currentId.value}`;
    const method = isNew.value ? "POST" : "PUT";

    const res = await fetch(url, {
      method,
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${authState.token}`,
        Accept: "application/json",
      },
      body: JSON.stringify(payload),
    });

    if (!res.ok) {
      const data = await res.json().catch(() => ({}));
      throw new Error(data.detail || "Failed to save project");
    }

    await res.json(); // we don't really need the body here
    await fetchProjects();
    showModal.value = false;
  } catch (e) {
    modalError.value = e.message || "Failed to save project";
  } finally {
    saving.value = false;
  }
}

function onStart(proj) {
  // Placeholder for now
  console.log("Start project", proj.id);
  // You can later route to a "working" page or mark submission started.
}

onMounted(() => {
  fetchProjects();
});
</script>

<style scoped>
.projects-page {
  max-width: 960px;
  margin: 0 auto;
}
.header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}
.header-actions button {
  padding: 0.4rem 0.8rem;
  border-radius: 0.4rem;
  border: none;
  background: #2563eb;
  color: #fff;
  font-weight: 600;
  cursor: pointer;
}
.projects-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 0.5rem;
}
.projects-table th,
.projects-table td {
  border: 1px solid #ddd;
  padding: 0.5rem 0.75rem;
  vertical-align: top;
}
.projects-table th {
  background: #f5f5f5;
  text-align: left;
}
.description-cell {
  max-width: 420px;
}
.actions-cell {
  text-align: center;
}
.actions-cell button {
  padding: 0.3rem 0.7rem;
  border-radius: 0.4rem;
  border: none;
  background: #2563eb;
  color: #fff;
  font-size: 0.875rem;
  cursor: pointer;
}
.error {
  color: #b91c1c;
  margin-top: 0.5rem;
}

/* Modal */

.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 40;
}
.modal {
  width: 100%;
  max-width: 420px;
  background: #fff;
  border-radius: 0.75rem;
  padding: 1.25rem 1.5rem;
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.18);
}
.modal h3 {
  margin-top: 0;
  margin-bottom: 0.75rem;
}
.modal form {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}
.modal label {
  display: flex;
  flex-direction: column;
  font-size: 0.9rem;
}
.modal input,
.modal textarea {
  margin-top: 0.25rem;
  padding: 0.35rem 0.5rem;
  border-radius: 0.4rem;
  border: 1px solid #ccc;
  font: inherit;
}
.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
  margin-top: 0.8rem;
}
.modal-actions button {
  padding: 0.4rem 0.8rem;
  border-radius: 0.4rem;
  border: none;
  cursor: pointer;
}
.modal-actions button[type="button"] {
  background: #e5e7eb;
}
.modal-actions button[type="submit"] {
  background: #2563eb;
  color: #fff;
}
</style>
