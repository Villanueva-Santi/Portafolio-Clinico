// src/store/user.js

import { defineStore } from 'pinia'
import api from '../services/api'

export const useUserStore = defineStore('user', {
  state: () => ({
    userData: null,   // Datos completos del usuario
    loading: false,   // Estado de carga
    error: null,      // Mensaje de error
  }),

  getters: {
    // Devuelve true si el usuario tiene sesión activa
    isAuthenticated: (state) => !!state.userData,

    // Devuelve el rol del usuario 
    userRole: (state) => state.userData?.rol || null,

    // Devuelve el nombre completo del usuario
    fullName: (state) =>
      state.userData
        ? `${state.userData.first_name} ${state.userData.last_name}`
        : '',
  },

  actions: {
    // Carga los datos del usuario autenticado desde la API
    async fetchUserData() {
      this.loading = true
      this.error = null
      try {
        const response = await api.get('user/profile/') 
        this.userData = response.data
      } catch (err) {
        console.error('Error al cargar los datos del usuario:', err)
        this.error = 'No se pudieron cargar los datos del usuario.'
      } finally {
        this.loading = false
      }
    },

    // Actualiza los datos del perfil del usuario
    async updateUserData(newData) {
      this.loading = true
      this.error = null
      try {
        const response = await api.put('user/profile/update/', newData)
        this.userData = response.data
      } catch (err) {
        console.error('Error al actualizar usuario:', err)
        this.error = 'Error al actualizar los datos del usuario.'
      } finally {
        this.loading = false
      }
    },

    // Guarda manualmente el usuario (por ejemplo, después de iniciar sesión)
    setUser(userData) {
      this.userData = userData
      this.error = null
    },

    // Limpia el estado (por ejemplo, al cerrar sesión)
    clearUserData() {
      this.userData = null
      this.error = null
    },
  },
})
