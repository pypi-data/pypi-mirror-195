<script setup>
import { ref } from "vue";

import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-icons/font/bootstrap-icons.css";
import AudioDownload from "./views/AudioDownload.vue";
import InputVideoNumber from "./views/InputVideoNumber.vue";

const stage = ref(0);
</script>

<template>
  <InputVideoNumber v-if="stage == 0" @change-stage="stage++" />
  <AudioDownload v-else />
</template>
