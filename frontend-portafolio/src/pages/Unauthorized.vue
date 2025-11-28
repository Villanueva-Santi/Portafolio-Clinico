<!-- src/pages/Unauthorized.vue -->
<template>
  <div class="flex flex-col items-center justify-center min-h-screen bg-gray-900 text-center text-white">
    <div class="p-10 rounded-2xl shadow-lg bg-gray-800 w-full max-w-4xl">
      <h1 class="text-5xl font-extrabold text-red-500 mb-6">
        Acceso no autorizado
      </h1>
      <RouterLink
        to="/home"
        class="text-blue-400 hover:underline text-lg"
      >
        Volver al inicio
      </RouterLink>
    </div>
  </div>
</template>
