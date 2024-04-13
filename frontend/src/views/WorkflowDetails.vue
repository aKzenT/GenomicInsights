<template>
<div class="container">
  <div class="Menu">
    <navigation/>
  </div>
  <div class="Content">


  <workflow-status/>
  </div>
</div>
</template>




<script>
import { defineComponent } from 'vue';

// Components

import Navigation from '../components/Menu.vue';
import WorkflowStatus from '../components/WorkflowStatus.vue';
export default defineComponent({
  name: 'WorkflowDetails',

  components: {
    Navigation,
    WorkflowStatus
  },


});


</script>

<style>
.container {
  display: grid; 
  grid-template-columns: 0.5fr 3fr
}

</style>
