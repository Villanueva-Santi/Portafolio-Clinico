<!-- src/components/estudiante/RegistroAutoevaluacion.vue -->

<template>
  <div class="space-y-6">
    <h1 class="text-2xl font-bold text-emerald-400">
      Registro de Autoevaluación
    </h1>

    <!-- Formulario principal -->
    <div class="bg-gray-800 p-6 rounded-2xl shadow-lg space-y-4">

      <!-- Semestre -->
      <div>
        <label class="block text-sm mb-1">Semestre</label>

        <!-- Lista completa -->
        <select
          v-model="form.semestre"
          class="w-1/5 p-2 rounded bg-gray-700 text-white"
        >
          <option value="">-- Seleccione el semestre --</option>
          <option v-for="n in 12" :key="n" :value="n">
            {{ n }}
          </option>
        </select>
      </div>

      <!-- Fecha -->
      <div>
        <label class="block text-sm mb-1">Fecha</label>
        <input
          type="date"
          v-model="form.fecha"
          class="w-1/5 p-2 rounded bg-gray-700 text-white"
        />
      </div>

      <!-- Procedimiento -->
      <div>
        <label class="block text-sm mb-1">Procedimiento</label>
        <select
          v-model="form.procedimiento"
          class="w-1/4 p-2 rounded bg-gray-700 text-white"
        >
          <option value="">-- Seleccione el procedimiento --</option>
          <option>Sutura</option>
          <option>Medicina Interna</option>
          <option>Cirugia</option>
        </select>
      </div>

        <div> 
        <label class="block text-sm mb-1">Profesor asociado al procedimiento</label>
        <select
          v-model="form.profesor"
          class="w-1/3 p-2 rounded bg-gray-700 text-white"
        >
          <option value="">-- Seleccione el profesor --</option>
          <option>profesor 1</option>
          <option>profesor 2</option>
          <option>profesor 3</option>
        </select>
      </div>

      <!-- Nivel Dreyfus + descripción dinámica -->
      <div class="flex items-start gap-6">
        <div>
          <label class="block text-sm mb-1">
            Nivel de Desempeño (Modelo Dreyfus y Dreyfus)
          </label>

          <!-- Se actualiza estado al cambiar -->
          <select
            v-model="form.nivel"
            class="w-1/1 p-2 rounded bg-gray-700 text-white"
          >
            <option value="">-- Seleccione un nivel --</option>
            <option value="NOVATO">Novato</option>
            <option value="PRINCIPIANTE_AVANZADO">Principiante Avanzado</option>
            <option value="COMPETENTE">Competente</option>
            <option value="PROFESIONAL">Profesional</option>
            <option value="EXPERTO">Experto</option>
          </select>
        </div>

        <!-- Cuadro dinámico obligatorio -->
        <div
        class="w-1/1 p-4 rounded-xl bg-gray-700 text-white border border-gray-500 shadow leading-relaxed space-y-2"
        v-if="descripcionNivel"
        v-html="descripcionNivel"        
        ></div>
      </div>

      <!-- ¿Cómo te sentiste? -->
      <div>
        <label class="block text-sm mb-1">¿Cómo te sentiste?</label>
        <textarea
          v-model="form.comoSeSintio"
          class="w-full p-3 rounded bg-gray-700 text-white"
          rows="3"
          placeholder="Lo que escribas en esta reflexión es importante para afianzar los conocimientos y prácticas..."
        ></textarea>
      </div>

      <!-- Principales aprendizajes -->
      <div>
        <label class="block text-sm mb-1">Principales aprendizajes de esta sesión</label>
        <textarea
          v-model="form.principalesAprendizajes"
          class="w-full p-3 rounded bg-gray-700 text-white"
          rows="3"
          placeholder="Describe lo aprendido durante este procedimiento..."
        ></textarea>
      </div>

      <!-- Botón -->
      <button
        class="w-full bg-emerald-600 hover:bg-emerald-700 text-white py-2 rounded transition"
        @click="confirmarGuardado"
      >
        Guardar Autoevaluación
      </button>
    </div>

    <!-- MODAL DE CONFIRMACIÓN -->
    <div
      v-if="mostrarConfirmacion"
      class="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center"
    >
      <div class="bg-gray-800 p-6 rounded-xl shadow-xl text-white space-y-4 w-96 text-center">
        <h2 class="text-lg font-semibold">Confirmar autoevaluación</h2>
        <p>¿Seguro que deseas registrar esta autoevaluación?</p>

        <div class="flex justify-between mt-4">
          <button
            class="px-4 py-2 bg-red-600 rounded hover:bg-red-700"
            @click="mostrarConfirmacion = false"
          >
            Cancelar
          </button>

          <button
            class="px-4 py-2 bg-emerald-600 rounded hover:bg-emerald-700"
            @click="guardarAutoevaluacion"
          >
            Confirmar
          </button>
        </div>
      </div>
    </div>

    <!-- MODAL DE ÉXITO -->
    <div
      v-if="mostrarExito"
      class="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center"
    >
      <div class="bg-gray-800 p-6 rounded-xl shadow-xl text-white space-y-4 w-96 text-center">
        <h2 class="text-lg font-semibold">Autoevaluación Registrada</h2>
        <p>La autoevaluación se ha guardado correctamente.</p>
        <button
          class="px-4 py-2 bg-emerald-600 rounded hover:bg-emerald-700 w-full"
          @click="mostrarExito = false"
        >
          OK
        </button>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { crearAutoevaluacion } from "@/services/api";   // IMPORTACIÓN ARRIBA
import { useAuthStore } from "@/store/auth";            // USO DEL STORE ARRIBA
const auth = useAuthStore(); 
//
// Estado reactivo del formulario
//
const form = ref({
  semestre: "",
  fecha: "",
  procedimiento: "",
  profesor: "",
  nivel: "",
  comoSeSintio: "",
  principalesAprendizajes: "",
});

//
// Diccionario de descripciones oficiales
//
const descripciones = {
  NOVATO:
    `
<strong>Novato:</strong> Este nivel se caracteriza por la falta de experiencia y conocimientos en una determinada área. 
Los novatos requieren instrucciones y reglas explícitas para llevar a cabo tareas, además de orientación por parte del profesor. 
<br>
<br>
<hr />
<br>
• Sigue reglas estrictas, descontextualizadas y literales.<br>
• No reconoce patrones; depende completamente del manual o del docente.<br>
• Actúa paso a paso, sin priorizar información.<br>
• En medicina: Corresponde al estudiante que necesita guías claras, listas de chequeo y supervisión directa.	
  `,

  PRINCIPIANTE_AVANZADO:
    `
<strong>Principiante Avanzado:</strong> En este nivel, los individuos tienen alguna experiencia práctica en el área y pueden 
empezar a tomar decisiones por sí mismos, aunque aún requieren reglas claras y orientación del profesor.
<br>
<br>
<hr />
<br>
• Comienza a identificar situaciones recurrentes o <strong>“Aspectos relevantes”</strong>.<br>
• Reconoce patrones simples.<br>
• Toma decisiones básicas con apoyo.<br>
• En medicina: Realiza tareas estructuradas con guía.
  `,
  COMPETENTE:
    `
<strong>Competente:</strong> Las personas en este nivel tienen suficiente experiencia práctica para tomar decisiones sin 
necesidad de seguir reglas explícitas. Son capaces de resolver problemas comunes y realizar tareas de manera eficiente.
<br>
<br>
<hr />
<br>
• Organiza la información, prioriza y planifica acciones.<br>
• Toma decisiones deliberadas y responsables.<br>
• Gestiona casos clínicos comunes.<br>
• En medicina: Puede llevar un caso completo, justificar decisiones y reflexionar sobre errores.
  `,
  PROFESIONAL:
     `
<strong>Profesional:</strong> Las personas alcanzan un alto nivel de experiencia práctica, lo que les permite adaptarse a 
situaciones imprevistas y manejar tareas complejas con éxito.
<br>
<br>
<hr />
<br>
• Percibe la situación de manera holística (Integral).<br>
• Aplica las reglas con flexibilidad y empieza a utilizar la intuición basada en la experiencia.<br>
• Anticipa problemas y adapta planes de acción.<br>
• En medicina: Resuelve casos complejos, integra múltiples protocolos y orienta a otros profesionales.
  `,
  EXPERTO:
  `
<strong>Experto:</strong> En este nivel, las personas tienen un conocimiento profundo y una amplia experiencia en el área que 
les permite tomar decisiones intuitivas y creativas en situaciones complejas.
<br>
<br>
<hr />
<br>
• Toma decisiones de forma fluida, automática e intuitiva.<br>
• Las reglas ya no guían su acción; actúa con base en modelos mentales profundos.<br>
• Reconoce patrones sutiles y responde rápidamente sin análisis explícito.<br>
• En medicina: Corresponde a un clínico altamente competente, líder y referente, con elevada conciencia situacional.
  `,
};

//
// Cálculo automático según el nivel seleccionado
//
const descripcionNivel = computed(() => descripciones[form.value.nivel] || "");

/* Estado para modales */
const mostrarConfirmacion = ref(false);
const mostrarExito = ref(false);

/* Función que abre el modal de confirmación */
const confirmarGuardado = () => {
  mostrarConfirmacion.value = true;
};

//
// Función que enviará la autoevaluación al backend (se conecta después)

// ---- GUARDAR AUTOEVALUACIÓN ----
const guardarAutoevaluacion = async () => {
  mostrarConfirmacion.value = false;  // # CAMBIO: cerrar modal de confirmación
  try {
    const payload = {
  //cedulaEstudiante: 1, // auth.user.id,                 
  //idProcedimientoRealizado: 1, //form.value.procedimiento_id, 
  nivelPercibido: form.value.nivel,
  comoSeSintio: form.value.comoSeSintio,
  principalesAprendizajes: form.value.principalesAprendizajes,
  fechaAutoevaluacion: form.value.fecha,          // ← obligatorio
};


  await crearAutoevaluacion(payload);

    mostrarExito.value = true;   

  } catch (error) {
    console.error("❌ Error al guardar autoevaluación:", error);
    alert("Hubo un error guardando la autoevaluación.");
  }
};

</script>
<style scoped>
</style>
