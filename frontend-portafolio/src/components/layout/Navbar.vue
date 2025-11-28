<!-- src/components/layout/Navbar.vue -->
<template>
  <nav class="bg-emerald-700 text-white px-6 py-3 flex justify-between items-center shadow-md">
    <div class="flex items-center space-x-3">
      <img src="@/assets/logo.svg" alt="Logo" class="h-8 w-8" />
      <span class="font-semibold text-lg">Portafolio Clínico</span>
    </div>

    <div class="flex items-center space-x-4">
      <!-- Evita error si auth.user aún no está cargado -->
      <span class="text-sm" v-if="auth.user">
        {{ auth.user.usuario }} ({{ auth.user.rol }})
      </span>

      <button
        @click="logout"
        class="bg-red-600 hover:bg-red-700 px-3 py-1 rounded text-sm font-bold transition"
      >
        Cerrar sesión
      </button>
    </div>
  </nav>
</template>

<script setup>
import { useAuthStore } from '@/store/auth'
import { useRouter } from 'vue-router'

const auth = useAuthStore()
const router = useRouter()

const logout = () => {
  auth.logout()
  router.push('/login')
}
</script>
