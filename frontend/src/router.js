import { createRouter, createWebHistory } from "vue-router";
import SplashView from "./views/SplashView.vue";
import AdminView from "./views/AdminView.vue";
import ProjectsView from "./views/ProjectsView.vue";
import { authState } from "./stores/auth";

const routes = [
  { path: "/", name: "splash", component: SplashView },
  { path: "/projects", name: "projects", component: ProjectsView },
  { path: "/admin", name: "admin", component: AdminView },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// simple guards
router.beforeEach((to, from, next) => {
  const { token, role } = authState;

  //check if logged in
  if (!token && to.name !== "splash") {
    return next({ name: "splash" });
  }

  //check if admin
  if (to.name === "admin" && role !== "admin") {
    return next({ name: "projects" });
  }

  next();
});

export default router;
