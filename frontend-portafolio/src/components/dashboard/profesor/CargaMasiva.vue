<!-- src/components/dashboard/profesor/CargaMasiva.vue -->

<template>
  <div class="space-y-6">

    <!-- Título -->
    <h1 class="text-2xl font-bold text-emerald-400">
      Carga Masiva
    </h1>

    <p class="text-gray-300">
      Seleccione un archivo CSV/Excel con los datos.  
      Se mostrará una vista previa antes de confirmar.
    </p>

    <!-- Contenedor visual estilo estudiante -->
    <div class="bg-gray-800 p-6 rounded-2xl shadow-lg space-y-4">

      <label
        for="fileUpload"
        class="flex items-center justify-center border-2 border-dashed border-emerald-500 rounded-xl h-32 cursor-pointer bg-gray-900 hover:bg-gray-700 transition"
      >
        <div class="text-center">
          <p class="text-emerald-300 font-semibold">Seleccionar archivo</p>
          <p class="text-gray-400 text-sm">(CSV o Excel)</p>
        </div>
      </label>
      <input id="fileUpload" type="file" class="hidden" @change="handleFileUpload" />

      <!-- Vista previa -->
      <div v-if="previewData.length" class="pt-4">

        <h2 class="text-lg font-semibold text-emerald-300 mb-2">
          Vista previa de registros:
        </h2>

        <div class="overflow-auto max-h-96 border border-gray-700 rounded-lg">
          <table class="table-auto w-full text-left border-collapse">
            <thead class="bg-gray-700 text-emerald-300 sticky top-0">
              <tr>
                <th
                  v-for="(col, index) in previewData[0]"
                  :key="index"
                  class="p-2 border border-gray-600"
                >
                  {{ col }}
                </th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(row, rindex) in previewData.slice(1)"
                :key="rindex"
                class="hover:bg-gray-900"
              >
                <td
                  v-for="(col, cindex) in row"
                  :key="cindex"
                  class="p-2 border border-gray-700"
                >
                  {{ col }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <button
          class="mt-4 px-6 py-2 bg-emerald-600 hover:bg-emerald-700 rounded transition"
          @click="confirmarCarga"
        >
          Confirmar carga
        </button>
      </div>
    </div>

    <!-- Modal de éxito -->
    <div
      v-if="modalExito"
      class="fixed inset-0 flex justify-center items-center bg-black bg-opacity-60"
    >
      <div class="bg-gray-800 p-6 rounded-xl text-center space-y-4">
        <h2 class="text-emerald-400 font-bold text-lg">✔ Carga exitosa</h2>
        <p class="text-gray-300">Los datos han sido registrados correctamente.</p>
        <button
          class="px-6 py-2 bg-emerald-600 hover:bg-emerald-700 rounded"
          @click="modalExito = false"
        >
          OK
        </button>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref } from "vue";

const previewData = ref([]);
const modalExito = ref(false);

const handleFileUpload = (event) => {
  const file = event.target.files[0];
  if (!file) return;

  const reader = new FileReader();

  reader.onload = (e) => {
    const text = e.target.result;

    previewData.value = text
      .trim()
      .split("\n")
      .map((row) => row.split(","));
  };

  reader.readAsText(file);
};

const confirmarCarga = () => {
  console.log("Datos procesados:", previewData.value);
  modalExito.value = true;
};
</script>
