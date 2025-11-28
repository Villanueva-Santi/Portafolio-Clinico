<!-- src/components/layout/Sidebar.vue -->
<template>
  <aside class="bg-gray-800 text-white w-64 min-h-screen p-5">
    <ul class="space-y-3">
      <li v-for="item in filteredMenu" :key="item.path"> 
        <router-link
          :to="item.path"
          class="block px-3 py-2 rounded hover:bg-gray-700 transition"
          :class="{ 'bg-gray-700': $route.path === item.path }" 
        >
          {{ item.name }}
        </router-link>
      </li>
    </ul>
  </aside>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from '@/store/auth'

const auth = useAuthStore()

const menu = [
  { name: 'Inicio', path: '/' },
  { name: 'Procedimientos', path: '/procedimientos', roles: ['Profesor', 'Estudiante'] },
  { name: 'Evaluaciones', path: '/evaluaciones', roles: ['Profesor', 'CoordinadorCurso'] },
  { name: 'Reportes', path: '/reportes', roles: ['Director', 'CoordinadorPractica'] },
  { name: 'Configuración', path: '/configuracion', roles: ['Director'] },
]

const filteredMenu = computed(() =>
  menu.filter(
    (item) => !item.roles || item.roles.includes(auth.user?.rol)
  )
)
</script>
