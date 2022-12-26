<template>
  <div class="content">
    <div v-loading="!isDataLoaded" class="wrapper-steps" id="wrapper-steps">
      <el-steps
        v-if="isDataLoaded"
        :active="active_step"
        finish-status="success"
        align-center
      >
        <el-step
          v-for="step in dag_task_order"
          :key="step"
          :title="step"
        ></el-step>
      </el-steps>
      <el-button
        id="downloadReport"
        type="primary"
        @click="downloadReport"
        :disabled="!isWorkflowFinished"
        >Download Report<el-icon class="el-icon--right"><Download /></el-icon
      ></el-button>
    </div>

    <div id="settings">
      <el-button
        class="settings"
        id="refreshButton"
        type="primary"
        style="margin-top: 12px"
        @click="refresh"
        >Refresh</el-button
      >
      <div id="switch" class="settings">
        <p>Automatic Reload</p>
        <el-switch
          v-model="isAutoReload"
          name="reload"
          inline-prompt
          active-text="On"
          inactive-text="Off"
          style="padding: 0 4px 0 0"
          @change="changeAutoReload"
        />
      </div>
    </div>
  </div>
</template>



<script>
import { Download } from "@element-plus/icons-vue";
import { ElNotification } from "element-plus";
import { ElMessage, ElMessageBox } from "element-plus";
import axios from "axios";
import { onBeforeUnmount } from "@vue/runtime-core";

export default {
  components: { Download },

  data: () => ({
    isAutoReload: true,
    isDataLoaded: false,
    dag_id: "",
    dag_run_id: "",
    loading: true,
    dag_data: [],
    reload_data: "",

    active: 0,
    active_step: 0,
    dag_task_order: [],
    isWorkflowFinished: false,
    file: "",
  }),

  methods: {
    refresh() {
      this.reload_workflow_data();
    },

    sleep(milliseconds) {
      return new Promise((resolve) => setTimeout(resolve, milliseconds));
    },

    getDagTasks() {
      axios
        .get(`http://localhost:8080/api/v1/dags/${this.dag_id}/tasks`, {
          auth: {
            username: "airflow",
            password: "airflow",
          },
          withCredentials: true,
        })
        .then((response) => {
          for (var index in response.data.tasks) {
            if (response.data.tasks[index].downstream_task_ids.length == 0) {
              this.dag_task_order.unshift(response.data.tasks[index].task_id);
            }
          }
          for (let step = 1; step < response.data.tasks.length; step++) {
            for (var index in response.data.tasks) {
              if (
                response.data.tasks[index].downstream_task_ids[0] ==
                this.dag_task_order[0]
              ) {
                this.dag_task_order.unshift(response.data.tasks[index].task_id);
                break;
              }
            }
          }
        });
    },

    async getDagTasksDetails() {
      this.isDataLoaded = false;
      await axios
        .get(
          `http://localhost:8080/api/v1/dags/${this.dag_id}/dagRuns/${this.dag_run_id}/taskInstances`,
          {
            auth: {
              username: "airflow",
              password: "airflow",
            },
            withCredentials: true,
          }
        )
        .then((response) => {
          this.dag_data = response.data.task_instances;
          var active_step = 0;

          for (var index in response.data.task_instances) {
            if (response.data.task_instances[index].state == "success") {
              active_step++;
            }
          }

          this.active_step = active_step;
          this.checkWorkflowFinished();
          this.isDataLoaded = true;
        });
    },

    reload_workflow_data() {
      this.getDagTasksDetails();
      this.checkWorkflowFinished();
    },

    changeAutoReload() {
      if (this.isAutoReload) {
        this.reload_data = setInterval(this.reload_workflow_data, 5000);
      } else {
        clearInterval(this.reload_data);
      }
    },

    checkWorkflowFinished() {
      if (this.active_step == this.dag_task_order.length) {
        this.isWorkflowFinished = true;
      }
    },

    downloadReport() {
      var report_filename =
        "report_" + this.file + "_" + this.dag_run_id + ".pdf";
      var report_filename_encoded = `${encodeURIComponent(report_filename)}`;
      axios
        .get(
          this.$frontendApi + "/downloadReportURL/" + report_filename_encoded,
          { responseType: "blob" }
        )
        .then((response) => {
          var fileURL = window.URL.createObjectURL(new Blob([response.data]));
          var fileLink = document.createElement("a");

          fileLink.href = fileURL;

          fileLink.setAttribute("download", report_filename);
          document.body.appendChild(fileLink);

          fileLink.click();
        });
    },
  },

  created() {
    this.dag_run_id = this.$route.query.dagRunId;
    this.file = this.$route.query.file;
    this.dag_run_id = this.dag_run_id.replace(" ", "+");
    this.dag_id = this.$route.query.dagId;
    this.getDagTasks();
    this.getDagTasksDetails();
    this.changeAutoReload();
    this.isDataLoaded = true;
  },

  beforeUnmount() {
    clearInterval(this.reload_data);
  },
};
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

.wrapper-steps {
  width: 80%;
  border: 2px lightgrey;
  border-style: solid;
  border-radius: 10px;
  min-height: 200px;
  position: relative;
  padding-top: 10px;
}
.wrapper-steps > * {
  margin: auto;
}

th {
  text-align: left;
}

#dataMissingTag {
  color: red;
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
  vertical-align: middle;
  margin-left: 5px;
}

.el-switch {
  margin-top: 12px;
}

#downloadReport {
  display: block;
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  margin-bottom: 12px;
}
</style>