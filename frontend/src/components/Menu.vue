<template>
  <el-row class="tactac">
    <el-col :span="20">
      <el-menu
        default-active="1"
        class="el-menu-vertical-demoo"
        @select="handleClick"
        router
      >
        <el-menu-item index="UploadData">
          <el-icon><DocumentAdd /></el-icon>
          <span>Upload Data</span>
        </el-menu-item>
        <el-menu-item index="StartAnalyse" >
          <el-icon><Promotion /></el-icon>
          <span>Start Analysis</span>
        </el-menu-item>
        <el-menu-item index="ActiveWorkflows">
          <el-icon><View /></el-icon>
          <span>Active Workflows</span>
        </el-menu-item>
      </el-menu>
    </el-col>
  </el-row>
</template>

<script lang="ts" setup>
import {
  Document,
  Menu as IconMenu,
  Location,
  Setting,
  DocumentAdd,
  Promotion,
  View
} from '@element-plus/icons-vue'

const handleClick = (key: string) => {
  console.log(key)
  switch (key){

    case "UploadData":
    case "StartAnalyse":
    case "ActiveWorkflows":

  }
 
}



</script>

<style scoped>
.el-menu {
  border-right: 0px;

}
.el-col {
  max-width: 100%;
}
</style>