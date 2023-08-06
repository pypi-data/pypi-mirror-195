<script setup>
import { onMounted, ref, inject, computed } from "vue";

import AudioCard from "../components/AudioCard.vue";
import TotalProgress from "../components/TotalProgress.vue";
import DownloadButton from "../components/DownloadButton.vue";

const axios = inject("axios");

const state_list = ref([]);

const auto_download = ref(false);

const counter = computed(() => {
  const total = state_list.value.length;
  let ready = 0;
  let downloading = 0;
  let finished = 0;
  state_list.value.forEach((s) => {
    if (s.number && s.title && s.total == 0) {
      ready++;
    } else if (s.received < s.total) {
      ready++;
      downloading++;
    } else if (s.total != 0 && s.received == s.total) {
      ready++;
      finished++;
    }
  });
  return {
    total: total,
    ready: ready,
    downloading: downloading,
    finished: finished,
  };
});

const progress_info = computed(() => {
  const { ready, downloading, finished, total } = counter.value;
  const fetch_info = "Fetching Information";
  const ready_info = "Ready";
  const download_info = "Downloading";
  const finished_info = "Downloads Complete";
  if (ready < total) {
    return { display: fetch_info, finished: ready, total: total };
  } else if (ready == total && !downloading && !finished) {
    return { display: ready_info, finished: ready, total: total };
  } else if (finished < total) {
    return {
      display: download_info,
      finished: finished,
      total: total,
    };
  } else if (finished == total) {
    return { display: finished_info, finished: finished, total: total };
  }
});

function start_download() {
  axios.get("/download");
}

onMounted(() => {
  setInterval(() => {
    axios.get("/progress").then((resp) => {
      state_list.value = resp.data;
    });
  }, 200);
});
</script>

<template>
  <div
    class="vh-100 vw-100 bg-body-secondary overflow-scroll d-flex flex-column position-relative"
  >
    <div class="container overflow-y-scroll flex-grow-1">
      <div class="row g-3 py-3">
        <div
          v-for="state in state_list"
          class="col-12 col-md-10 offset-md-1 col-xl-6 offset-xl-0"
        >
          <AudioCard v-bind="state"></AudioCard>
        </div>
      </div>
    </div>
    <DownloadButton
      @enable-download="auto_download = true"
      v-if="!auto_download && counter.ready == counter.total"
      @click="start_download"
    ></DownloadButton>
    <TotalProgress v-else v-bind="progress_info"></TotalProgress>
  </div>
</template>
