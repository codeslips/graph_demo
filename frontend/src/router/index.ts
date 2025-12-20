import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'home',
    component: () => import('@/views/HomeView.vue')
  },
  {
    path: '/tasks',
    name: 'tasks',
    component: () => import('@/views/TaskListView.vue')
  },
  {
    path: '/tasks/:id',
    name: 'task-detail',
    component: () => import('@/views/TaskDetailView.vue')
  },
  {
    path: '/graph/:id',
    name: 'graph',
    component: () => import('@/views/GraphView.vue')
  },
  {
    path: '/media',
    name: 'media',
    component: () => import('@/views/MediaView.vue')
  },
  {
    path: '/media/:platform/:entityType/:id',
    name: 'media-detail',
    component: () => import('@/views/MediaDetailView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router

