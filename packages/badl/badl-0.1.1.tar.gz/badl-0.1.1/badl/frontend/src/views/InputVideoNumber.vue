<script setup>
import { ref, onMounted, inject } from "vue";

const emit = defineEmits(["change-stage"]);

const input = ref(null);
const nvlist = ref("");

const axios = inject("axios");

const path = ref("");

onMounted(() => {
  input.value.focus();
});

function sendNVList() {
  axios.post("/video", { nvlist: nvlist.value });
  emit("change-stage");
}

function get_path() {
  axios.get("/path").then(({ data }) => {
    path.value = data;
    input.value.focus();
  });
}
</script>

<template>
  <div class="container-fluid vh-100 bg-body-secondary d-flex flex-column p-3">
    <div class="mb-3 row g-2">
      <div class="col-auto">
        <label class="col-form-label">Download Path:</label>
      </div>
      <div class="col">
        <input class="form-control" type="text" v-model="path" />
      </div>
      <div class="col-auto">
        <button class="btn btn-primary" @click="get_path">Choose</button>
      </div>
    </div>
    <textarea
      ref="input"
      v-model="nvlist"
      class="form-control form-control-lg flex-grow-1"
      placeholder="Input AV/BV numbers here."
    ></textarea>
    <button @click="sendNVList" type="button" class="btn btn-primary mt-3">
      OK
    </button>
  </div>
</template>
