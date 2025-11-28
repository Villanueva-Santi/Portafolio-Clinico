<!-- src/components/dashboard/DashboardEstudiante.vue -->
<template>
  <div class="min-h-screen bg-gray-900 text-white flex flex-col items-center p-8">
    <h1 class="text-3xl font-bold text-emerald-400 mb-2">Bienvenido(a), {{ displayName }}</h1> <!-- #️⃣ CAMBIO: ahora usa displayName -->
    <p class="text-gray-300 mb-10">Visualiza tu progreso clínico, autoevalúate y revisa la retroalimentación de tus docentes.</p>

    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 w-full max-w-5xl">
      <router-link
        v-for="item in menuItems"
        :key="item.path"
        :to="item.path"
        class="bg-gray-800 hover:bg-emerald-600 transition rounded-2xl shadow-lg p-6 flex flex-col items-center justify-center text-center cursor-pointer"
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
import { BookOpen, BarChart2, FileText, MessageSquare } from 'lucide-vue-next'
import { useAuthStore } from '@/store/auth'

const auth = useAuthStore()

// Nombre visible en el dashboard
// Se recoge desde el backend (auth.user) y se usa en el template como displayName
const displayName = computed(() => {
  return (
    auth.user?.nombre1 || 
    auth.user?.usuario || 
    'Estudiante'
  )
})

const menuItems = ref([
  {
    title: 'Autoevaluación',
    desc: 'Registra tus reflexiones sobre tus prácticas clínicas.',
    path: '/estudiante/autoevaluacion',
    icon: BookOpen,
  },
  {
    title: 'Curva de Aprendizaje',
    desc: 'Observa tu progreso con base en el modelo Dreyfus y Dreyfus.',
    path: '/estudiante/curva',
    icon: BarChart2,
  },
  {
    title: 'Histórico de Procedimientos',
    desc: 'Consulta tus procedimientos anteriores y su evaluación.',
    path: '/estudiante/historico',
    icon: FileText,
  },
  {
    title: 'Retroalimentación del Profesor',
    desc: 'Lee los comentarios y observaciones de tus docentes.',
    path: '/estudiante/retroalimentacion',
    icon: MessageSquare,
  },
])
</script>
