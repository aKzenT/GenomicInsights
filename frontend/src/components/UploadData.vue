<template>
<div  class="content">
    
    <div class="wrapper-upload">

          <el-upload
    class="upload-demo"
    drag
    action='http://localhost:5001/upload/'
    multiple
  >
    <el-icon class="el-icon--upload"><upload-filled /></el-icon>
    <div class="el-upload__text">
      Drop file here or <em>click to upload</em>
    </div>
    <template #tip>
      <div class="el-upload__tip">
       
      </div>
    </template>
  </el-upload>

    </div>
 
</div>
</template>

<script setup >
import { UploadFilled } from '@element-plus/icons-vue'

</script>

<script>
export default {
 
data() {
    return {
    }
},
}

</script>


<style scoped>

.selectAnalyse {
  height: 200px;
}
.el-steps {
  width: 80%;
}

.el-steps {
  width: 80%;
}

.wrapper-upload {
  width: 80%;
  border: 2px lightgrey;
  border-style: solid;
  border-radius: 10px;
  min-height: 200px;
   position: relative;

 
}
.wrapper-steps > * {
   margin:auto;
}

th {
  text-align: left;
}

#dataMissingTag {

  color: red

}

#el-switch.mb-2 {
    margin-left: auto;
}

#settings { 
display: flex; 

width: 80%;
}
#switch {
    width: fit-content;
    margin-left: auto;
}

.settings {
    display: inline-block; 
}

#switch > * {
    display: inline-block;
    vertical-align:middle; 
}

.el-switch {
    margin-top: 12px
}

#downloadReport{
  
    display: block;
    position:absolute;
    bottom: 0;
    left: 0;
    right: 0;
    margin-bottom: 12px;

}
</style>