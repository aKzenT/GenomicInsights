<template>
<div class="container">
  <div class="Menu">
    <navigation/>
  </div>
  <div class="Content">
  </div>
</div>
</template>




<script>
import { defineComponent } from 'vue';

// Components

import Navigation from '../components/Menu.vue';

export default defineComponent({
  name: 'HomeView',

  components: {
    Navigation
  },
});
</script>

<style>
.container {
  display: grid; 
  grid-template-columns: 0.5fr 3fr
}

</style>