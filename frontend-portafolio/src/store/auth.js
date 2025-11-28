// src/store/auth.js
import { defineStore } from 'pinia'
import api from '../services/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: JSON.parse(localStorage.getItem('user')) || null,
    rol: localStorage.getItem('rol') || null,
    token: localStorage.getItem('token') || null,
    isAuthenticated: !!localStorage.getItem('token'),
  }),

  actions: {
    async login(usuario, contrasena) {
      try {
        const response = await api.post('/login/', { usuario, contrasena })

        // Backend devuelve:
        // "usuario": "santiago123"
        // "rol": "estudiante"
        // "token": "xxxxx"
        const token = response.data.token

        const user = {
          usuario: response.data.usuario,   
          rol: response.data.rol || null,   
        }

        const rol =
          response.data.rol ||
          response.data.user?.rol ||
          response.data.usuario?.rol ||
          response.data.usuario?.idFuncion?.nombreFuncion ||
          null

        if (!token) throw new Error('No se recibió token del servidor.')

        // Actualizar estado
        this.token = token
        this.user = user                            
        this.rol = rol ? rol.toLowerCase().trim() : null
        this.isAuthenticated = true

        // Guardar en localStorage
        localStorage.setItem('token', token)
        localStorage.setItem('user', JSON.stringify(user))  
        localStorage.setItem('rol', this.rol)

        api.defaults.headers.common['Authorization'] = `Token ${token}`

        return response.data
      } catch (error) {
        console.error('Error en login:', error.response?.data || error.message)
        this.logout()
        throw new Error(error.response?.data?.error || 'Error de autenticación.')
      }
    },

    logout() {
      this.user = null
      this.rol = null
      this.token = null
      this.isAuthenticated = false
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      localStorage.removeItem('rol')
      delete api.defaults.headers.common['Authorization']
    },
  },
})

// Restaurar token al recargar
if (localStorage.getItem('token')) {
  api.defaults.headers.common['Authorization'] = `Token ${localStorage.getItem('token')}`
}
