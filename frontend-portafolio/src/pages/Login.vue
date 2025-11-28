<!---- src/pages/Login.vue  -->
<template>
  <div class="flex items-center justify-center w-screen h-screen bg-gray-100">
    <div class="bg-white shadow-xl rounded-2xl p-10 w-full max-w-3xl text-center">

      <img 
        src="@/assets/Logo_unisimon.png"
        alt="Logo Universidad Simón Bolívar"
        class="mx-auto mb-6 w-25"  
      />

      <h1 class="text-3xl font-bold text-emerald-600 mb-3">E-Portafolio Ser Médico Unisimon</h1>
      
      <p class="text-gray-600 mb-6">
        <!-- Inicia sesión con tus credenciales institucionales para continuar. -->
      </p>

      <!-- LoginForm -->
      <LoginForm />
    </div>
  </div>
</template>

<script setup>
import LoginForm from '@/components/auth/LoginForm.vue'
</script>

