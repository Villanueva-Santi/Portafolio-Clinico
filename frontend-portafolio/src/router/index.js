// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/store/auth'

// Importación de páginas
import Login from '@/pages/Login.vue'
import Home from '@/pages/Home.vue'
import Unauthorized from '@/pages/Unauthorized.vue'

// Importación de dashboards
import DashboardDirector from '@/components/dashboard/DashboardDirector.vue'
import DashboardCoordPractica from '@/components/dashboard/DashboardCoordPractica.vue'
import DashboardCoordCurso from '@/components/dashboard/DashboardCoordCurso.vue'
import DashboardProfesor from '@/components/dashboard/DashboardProfesor.vue'
import DashboardEstudiante from '@/components/dashboard/DashboardEstudiante.vue'

// Importación del layout principal
import MainLayout from '@/components/layout/MainLayout.vue'

// Importación de submódulos del estudiante
import RegistroAutoevaluacion from '@/components/dashboard/estudiante/RegistroAutoevaluacion.vue' // #️⃣
import CurvaAprendizaje from '@/components/dashboard/estudiante/CurvaAprendizaje.vue' // #️⃣
import HistoricoProcedimientos from '@/components/dashboard/estudiante/HistoricoProcedimientos.vue' // #️⃣
import RetroalimentacionProfesor from '@/components/dashboard/estudiante/RetroalimentacionProfesor.vue' // #️⃣

// Importación de submódulos del profesor
import EvaluarEstudiante from '@/components/dashboard/profesor/EvaluarEstudiante.vue'             // #️⃣
import HistoricoEvaluaciones from '@/components/dashboard/profesor/HistoricoEvaluaciones.vue'     // #️⃣
import RetroalimentacionesProfesor from '@/components/dashboard/profesor/RetroalimentacionesProfesor.vue' // #️⃣
import CargaMasiva from '@/components/dashboard/profesor/CargaMasiva.vue'                       // #️⃣


const routes = [
  { path: '/', component: Home },
  { path: '/home', component: Home }, 
  { path: '/login', component: Login },
  { path: '/unauthorized', component: Unauthorized },

  // Rutas protegidas usando el layout principal
  {
    path: '/director',
    component: MainLayout,
    meta: { requiresAuth: true, role: 'director' },
    children: [{ path: '', component: DashboardDirector }]
  },
  {
    path: '/coord-practica',
    component: MainLayout,
    meta: { requiresAuth: true, role: 'coordinador de práctica' },
    children: [{ path: '', component: DashboardCoordPractica }]
  },
  {
    path: '/coord-curso',
    component: MainLayout,
    meta: { requiresAuth: true, role: 'coordinador de curso' },
    children: [{ path: '', component: DashboardCoordCurso }]
  },
  {
    path: '/profesor',
    component: MainLayout,
    meta: { requiresAuth: true, role: 'profesor' },
    children: [
      { path: '', component: DashboardProfesor },

      { path: 'evaluar', component: EvaluarEstudiante },                  
      { path: 'historico-evaluaciones', component: HistoricoEvaluaciones }, 
      { path: 'retroalimentaciones', component: RetroalimentacionesProfesor }, 
      { path: 'carga-masiva', component: CargaMasiva },
    ]
  },

  // Rutas del estudiante con subrutas internas
  {
    path: '/estudiante',
    component: MainLayout,
    meta: { requiresAuth: true, role: 'estudiante' },
    children: [
      { path: '', component: DashboardEstudiante }, // Dashboard principal
      { path: 'autoevaluacion', component: RegistroAutoevaluacion }, // #️⃣
      { path: 'curva', component: CurvaAprendizaje }, // #️⃣
      { path: 'historico', component: HistoricoProcedimientos }, // #️⃣
      { path: 'retroalimentacion', component: RetroalimentacionProfesor } // #️⃣
    ]
  },

  // Ruta 404 o fallback
  { path: '/:pathMatch(.*)*', component: Unauthorized }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Autenticación y validación por rol
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  if (to.meta.requiresAuth) {
    if (!authStore.token) {
      console.warn('⚠️ No hay token activo. Redirigiendo a login...')
      return next('/login')
    }

    let userRole =
      authStore.rol ||
      authStore.user?.rol ||
      authStore.user?.idFuncion?.nombreFuncion ||
      ''
    userRole = userRole.toString().trim().toLowerCase()
    const routeRole = to.meta.role?.toString().trim().toLowerCase() || ''

    if (routeRole && routeRole !== userRole) {
      console.warn(
        `⚠️ Acceso denegado. Rol requerido: ${routeRole}, rol del usuario: ${userRole}`
      )
      return next('/unauthorized')
    }
  }

  next()
})

export default router
