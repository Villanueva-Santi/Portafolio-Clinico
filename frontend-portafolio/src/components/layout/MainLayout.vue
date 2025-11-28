<!-- src/components/layout/MainLayout.vue -->
<template>
  <div class="flex min-h-screen bg-gray-900 text-white">
    <!-- Sidebar -->
    <aside class="w-64 bg-gray-800 p-4">
      <h2 class="text-lg font-semibold mb-4">
        Menú
      </h2>

      <nav>
        <!-- DASHBOARD PROFESOR -->
        <router-link
          v-if="auth.rol === 'profesor'"
          to="/profesor"
          class="block py-1 hover:text-emerald-400"
        >
          Dashboard Profesor
        </router-link>

        <!-- DASHBOARD ESTUDIANTE -->
        <router-link
          v-if="auth.rol === 'estudiante'"
          to="/estudiante"
          class="block py-1 hover:text-emerald-400"
        >
          Dashboard Estudiante
        </router-link>

        <!-- SUBMENÚ ESTUDIANTE -->
        <div v-if="auth.rol === 'estudiante'" class="mt-2 ml-4 space-y-1"> 
          <router-link                                         
            to="/estudiante/autoevaluacion"                   
            class="block text-sm py-1 hover:text-emerald-300" 
          >
            Autoevaluación                                     
          </router-link>

          <router-link                                         
            to="/estudiante/curva"                            
            class="block text-sm py-1 hover:text-emerald-300" 
          >
            Curva de Aprendizaje                               
          </router-link>

          <router-link                                         
            to="/estudiante/historico"                        
            class="block text-sm py-1 hover:text-emerald-300" 
          >
            Histórico de Procedimientos                        
          </router-link>

          <router-link                                         
            to="/estudiante/retroalimentacion"                
            class="block text-sm py-1 hover:text-emerald-300" 
          >
            Retroalimentación del Profesor                     
          </router-link>
        </div>

        
        <!-- SUBMENÚ PROFESOR -->
        <div v-if="auth.rol === 'profesor'" class="mt-2 ml-4 space-y-1"> 

        <router-link
        to="/profesor/evaluar"                                   
        class="block text-sm py-1 hover:text-emerald-300"
        >
        Retroalimentar Estudiante                                         
        </router-link>

        <router-link
        to="/profesor/historico-evaluaciones"                    
        class="block text-sm py-1 hover:text-emerald-300"
        >
        Histórico de Evaluaciones                                  
        </router-link>

        <router-link
        to="/profesor/retroalimentaciones"                        
        class="block text-sm py-1 hover:text-emerald-300"
        >
        Retroalimentaciones Emitidas                                
        </router-link>

        <router-link
        to="/profesor/carga-masiva"                        
        class="block text-sm py-1 hover:text-emerald-300"
        >
        Carga Masiva                                
        </router-link>

        </div>

        <!-- Cerrar sesión -->
        <button
          @click="logout"
          class="block py-1 text-left w-full hover:text-red-400 mt-4"
        >
          Cerrar sesión
        </button>
      </nav>
    </aside>

    <!-- Contenido principal -->
    <main class="flex-1 p-6">
      <router-view />
    </main>
  </div>
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
