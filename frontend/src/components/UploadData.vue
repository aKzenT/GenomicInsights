<template>
  <div class="hdfs-browser">
    <h3>Select a directory or file from HDFS:</h3>

    <!-- Navigation bar -->
    <div v-if="currentDir !== 'microbiome-data'" class="navigation">
      <el-button @click="navigateUp" icon="el-icon-arrow-left" type="info" plain>
        Back to previous directory
      </el-button>
    </div>

    <!-- Directory/File List -->
    <ul class="file-list">
      <li 
        v-for="file in currentDirFiles" 
        :key="file.pathSuffix"
        :class="{ selected: selectedFile === file.pathSuffix }"
        @click="handleClick(file)"
        @dblclick="navigateDown(file)"
      >
        <span class="list-item">
          <Folder v-if="file.type === 'DIRECTORY'" class="icon" />
          <Document v-else class="icon" />
          <strong v-if="file.type === 'DIRECTORY'">{{ file.pathSuffix }}</strong>
          <span v-else>{{ file.pathSuffix }}</span>
        </span>
      </li>
    </ul>

    <!-- Upload Button -->
    <el-button 
      v-if="selectedFile" 
      :disabled="uploadInProgress"
      @click="uploadSelected" 
      type="primary"
      class="upload-button"
    >
      Upload selected item
    </el-button>

    <!-- Upload feedback -->
    <div class="upload-feedback">
      <el-alert
        v-if="uploadSuccessful === true"
        title="Upload successful!"
        type="success"
        show-icon
        :closable="false"
      />
      <el-alert
        v-else-if="uploadSuccessful === false"
        title="Upload failed!"
        type="error"
        show-icon
        :closable="false"
      />
    </div>
  </div>
</template>

<script>
import { Folder, Document } from '@element-plus/icons-vue'
export default {
  data() {
    return {
      currentDir: 'microbiome-data',
      currentDirFiles: [],
      selectedFile: null, 
      uploadSuccessful: null,
      isDblClick: true,
    };
  },
  components: {
    Folder,
    Document
  },
  methods: {
    async fetchHdfsFiles(dir) {
      try {
        const encodedDir = encodeURIComponent(dir);
        const response = await fetch(`http://localhost:5000/getHDFSFiles/${encodedDir}`);
        const files = await response.json();
        this.currentDirFiles = files.files; 
      } catch (error) {
        console.error('Error getting the HDFS files:', error);
      }
    },

    navigateDown(file) {
      if (file.type === 'DIRECTORY') {
        if (this.currentDir + '/' + file.pathSuffix !== this.currentDir) {
          this.currentDir += `/${file.pathSuffix}`;
          this.fetchHdfsFiles(this.currentDir);
        }
      }
    },

    handleClick(file) {
      this.isDblClick = !this.isDblClick;
      setTimeout(() => {
        if(!this.isDblClick) {
          this.select(file);
        }
        this.isDblClick = true;
      }, 200);
    },

    select(file) {
      this.selectedFile = file.pathSuffix;
    },

    navigateUp() {
      const newDir = this.currentDir.substring(0, this.currentDir.lastIndexOf('/'));
      this.currentDir = newDir || '/';
      this.fetchHdfsFiles(this.currentDir);
    },

    async uploadSelected() {
      if (this.selectedFile) {
        try {
          const encodedDir = encodeURIComponent(`${this.currentDir}/${this.selectedFile}`);
          const response = await fetch(`http://localhost:5000/downloadFromHDFS/${encodedDir}`);
          this.uploadSuccessful = true;
          this.selectedFile = null;
          setTimeout(() => {
            this.uploadSuccessful = null;
          }, 5000);
        } catch (error) {
          console.error('Error uploading the HDFS files:', error);
        }
      }
    },
  },

  // Initial loading of microbiome-directory
  created() {
    this.fetchHdfsFiles(this.currentDir);
  },
};
</script>

<style scoped>
li {
  cursor: pointer;
}

.hdfs-browser {
  border: 1px solid #dcdfe6;
  border-radius: 8px;
  padding: 24px;
  max-width: 600px;
  background: #fafafa;
  margin: 0 auto;
}

.navigation {
  margin-bottom: 16px;
}

.file-list {
  list-style: none;
  padding: 0;
  margin-bottom: 20px;
  border: 1px solid #ebeef5;
  border-radius: 4px;
}

.icon {
  margin-right: 6px;
  font-size: 16px;
  width: 25px;
  height: 25px;
}

.list-item {
  display: flex;
  align-items: center;
}

.file-list li:hover {
  background-color: #f5f7fa;
}

.file-list li.selected {
  background-color: #ffe58f;
}

.upload-button {
  margin-top: 12px;
}

.upload-feedback {
  margin-top: 16px;
}
</style>
