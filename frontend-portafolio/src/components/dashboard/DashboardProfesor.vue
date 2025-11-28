<!-- src/components/dashboard/DashboardProfesor.vue -->

<template>
  <div class="min-h-screen bg-gray-900 text-white flex flex-col items-center p-8">
    <h1 class="text-3xl font-bold text-emerald-400 mb-2">
      Bienvenido(a), {{ displayName }}       <!-- #️⃣ -->
    </h1>

    <p class="text-gray-300 mb-10">
      Desde aquí puede evaluar estudiantes, registrar retroalimentación y consultar el historial de evaluaciones.
    </p>

    <!-- MENÚ INTERNO -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 w-full max-w-5xl">
      <router-link
        v-for="item in menuItems"
        :key="item.path"
        :to="item.path"
        class="bg-gray-800 hover:bg-emerald-600 transition rounded-2xl shadow-lg p-6 flex flex-col items-center justify-center cursor-pointer"
      >
        <component :is="item.icon" class="w-10 h-10 mb-3 text-emerald-400" />
        <h2 class="text-lg font-semibold text-white mb-1">{{ item.title }}</h2>
        <p class="text-gray-400 text-sm">{{ item.desc }}</p>
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { CheckCircle, NotebookPen, ClipboardList, Upload } from 'lucide-vue-next'   // #️⃣
import { useAuthStore } from '@/store/auth'

const auth = useAuthStore()

// NOMBRE QUE SE MUESTRA
const displayName = computed(() =>
  auth.user?.nombre1 ||
  auth.user?.usuario ||
  'Profesor'
)

const menuItems = ref([
  {
    title: 'Retroalimentar Estudiante',
    desc: 'Registrar evaluación y nivel de competencia.',
    path: '/profesor/evaluar',
    icon: CheckCircle,
  },
  {
    title: 'Histórico de Evaluaciones',
    desc: 'Revisar evaluaciones realizadas previamente.',
    path: '/profesor/historico-evaluaciones',
    icon: ClipboardList,
  },
  {
    title: 'Retroalimentaciones Emitidas',
    desc: 'Consultar comentarios registrados para los estudiantes.',
    path: '/profesor/retroalimentaciones',
    icon: NotebookPen,
  },
  {
    title: 'Carga Masiva',                         
    desc: 'Subir registros en lote desde archivo.',
    path: '/profesor/carga-masiva',                
    icon: Upload,                                  
  },
])
</script>
