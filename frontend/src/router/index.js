import { createRouter, createWebHistory } from "vue-router";
import LoginView from "../views/LoginView.vue";
import UserInfoView from "../views/UserInfoView.vue";
import MenuView from "../views/MenuView.vue";
import PrepareView from "../views/PrepareView.vue";
import HomeView from "../views/HomeView.vue";
import PreView from "../views/PreView.vue";
import ContestantView from "../views/ContestantView.vue";
import ContestRaceView from "../views/ContestRaceView.vue";
import store from "../store";

const childRoutes = Array.from(JSON.parse(import.meta.env.VITE_APP_CATEGORIES),(category, index) => {
  return {
    path: category.en,
    name: `${category.en.charAt(0).toUpperCase() + category.en.slice(1)}View`,
    component: ContestantView,
    props: {
      pageNum: index
    }
  }
})

childRoutes.push({
  path: "Preview",
  name: "PreView",
  component: PreView
})

const childRaceRoutes = Array.from(JSON.parse(import.meta.env.VITE_APP_CATEGORIES),(category, index) => {
  return {
    path: category.en,
    name: `${category.en.charAt(0).toUpperCase() + category.en.slice(1)}RaceView`,
    component: ContestRaceView,
    props: {
      pageNum: index
    }
  }
})

const routes = [
  {
    path: "/prepare",
    name: "PrepareView",
    component: PrepareView,
  },
  {
    path: "/userinfo",
    name: "UserInfoView",
    component: UserInfoView,
  },
  {
    path: "/login",
    name: "LoginView",
    component: LoginView,
  },
  {
    path: "/",
    name: "MenuView",
    component: MenuView,
    meta: { requiresAuth: true },
  },
  {
    path: "/home",
    name: "HomeView",
    component: HomeView,
    meta: { requiresAuth: true },
    children: childRoutes
  },
  {
    path: "/race",
    name: "RaceView",
    meta: { requiresAuth: true },
    children: childRaceRoutes
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

router.beforeEach((to, from, next) => {
  // 讀取一開始於Login寫入的Token
  const token = store.state.token;

  // 有token又到登入頁，就導向HomePage
  if (to.name === "LoginView" && token) {
    next({ name: "MenuView" });
  } else if (to.name === "HomeView" && token) {
    next({ name: "SingView" });
  }
  // 判斷有要求權限的頁面檢查token
  else if (to.matched.some((res) => res.meta.requiresAuth)) {
    if (!token) {
      next({ name: "LoginView" });
    } else {
      next();
    }
  } else {
    next();
  }
});

export default router;
