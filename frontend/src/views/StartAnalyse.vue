<template>
<div class="container">

  <div class="Menu">
    <navigation/>
  </div>
  <div class="Content">
    <select-analyse/>
  </div>
</div>
</template>




<script>
import { defineComponent } from 'vue';

// Components
import SelectAnalyse from '../components/SelectAnalyse.vue';
import Navigation from '../components/Menu.vue';

export default defineComponent({
  name: 'StartAnalyse',

  components: {
    SelectAnalyse,
    Navigation
  },
});
</script>

<style>
.container {
  display: grid; 
  grid-template-columns: 20% 60% 20%
}
</style>