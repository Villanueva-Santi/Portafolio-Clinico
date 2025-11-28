<!-- src/components/auth/LoginForm.vue -->
<template>
  <div class="flex items-center justify-center h-full bg-transparent"> 
    <form @submit.prevent="handleLogin" class="bg-gray-800 p-8 rounded-2xl shadow-lg w-full">
      <h1 class="text-2xl text-center text-white mb-6 font-bold">Iniciar Sesión</h1>

      <!-- Campos del backend: usuario y contrasena -->
      <input
        v-model="usuario"
        id="usuario"
        name="usuario"
        type="text"
        placeholder="Usuario"
        class="w-full p-2 mb-4 rounded bg-gray-700 text-white focus:outline-none focus:ring-2 focus:ring-emerald-500"
        :disabled="loading"
      />

      <input
        v-model="contrasena"
        id="contrasena"
        name="contrasena"
        type="password"
        placeholder="Contraseña"
        class="w-full p-2 mb-4 rounded bg-gray-700 text-white focus:outline-none focus:ring-2 focus:ring-emerald-500"
        :disabled="loading"
      />

      <button
        type="submit"
        class="w-full bg-emerald-600 hover:bg-emerald-700 text-white font-bold py-2 rounded transition disabled:opacity-50"
        :disabled="loading"
      >
        <span v-if="!loading">Entrar</span>
        <span v-else>Cargando...</span>
      </button>

      <p v-if="errorMessage" class="text-red-500 text-sm text-center mt-4">
        {{ errorMessage }}
      </p>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '../../store/auth'
import { useRouter } from 'vue-router'

const usuario = ref('')
const contrasena = ref('')
const loading = ref(false)
const errorMessage = ref('')
const router = useRouter()
const auth = useAuthStore()

const handleLogin = async () => {
  errorMessage.value = ''
  loading.value = true

  try {
    // #️⃣ Llamamos al método login del store
    const data = await auth.login(usuario.value, contrasena.value)

    // #️⃣ Intentamos obtener el rol desde distintas fuentes
    let rol = auth.rol || data?.rol || data?.usuario?.idFuncion?.nombreFuncion

    // #️⃣ Normalizamos el rol (quitamos espacios, pasamos a minúsculas)
    rol = rol ? rol.toString().trim().toLowerCase() : null

    if (!rol) throw new Error('No se pudo determinar el rol del usuario.')

    // #️⃣ Redirección según el rol
    switch (rol) {
      case 'director':
      case 'director de programa':
        router.push('/director')
        break
      case 'coordinadorpractica':
      case 'coordinador de practica':
      case 'coordinador de práctica':
        router.push('/coord-practica')
        break
      case 'coordinadorcurso':
      case 'coordinador de curso':
        router.push('/coord-curso')
        break
      case 'profesor':
        router.push('/profesor')
        break
      case 'estudiante':
        router.push('/estudiante')
        break
      default:
        console.warn('⚠️ Rol desconocido:', rol)
        router.push('/unauthorized')
    }
  } catch (error) {
    console.error('⚠️ Error en inicio de sesión:', error)
    if (error.response?.status === 400 || error.response?.status === 401) {
      errorMessage.value = 'Usuario o contraseña incorrectos. Inténtalo nuevamente.'
    } else {
      errorMessage.value = 'Error de conexión con el servidor.'
    }
  } finally {
    loading.value = false
  }
}
</script>
