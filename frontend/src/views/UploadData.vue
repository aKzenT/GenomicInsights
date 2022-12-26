<template>
<div class="container">
  <div class="Menu">
    <navigation/>
  </div>
  <div class="Content">
    <upload-files/>
  </div>
</div>
</template>




<script>
import { defineComponent } from 'vue';

// Components

import Navigation from '../components/Menu.vue';
import UploadFiles from '../components/UploadData.vue';
import SelectAnalyse from '../components/SelectAnalyse.vue';

export default defineComponent({
  name: 'UploadData',

  components: {
  
    Navigation,
    UploadFiles,
    SelectAnalyse
  },
});




</script>

<style>
.container {
  display: grid; 
  grid-template-columns: 0.5fr 3fr
}

</style>