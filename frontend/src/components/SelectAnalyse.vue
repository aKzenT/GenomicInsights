<template>
  <div class="content">
    <div class="wrapper-steps">
      <el-steps :active="active" finish-status="success" align-center>
        <el-step title="Select Workflow"> </el-step>

        <el-step title="Select File" />
        <el-step title="Submit" />
      </el-steps>

      <el-form v-if="active === 0 && isDataLoaded">
        <div class="stepper-form" id="fileSelect">
          <input
            class="searchInput"
            type="text"
            id="myInput"
            @keyup="searchWorkflows"
            placeholder=" &#x1F50D; Search for Workflows..."
            :prefix-icon="Serach"
          />
          <table id="selectWorkflowTable">
            <tr class="header">
              <th style="width: 10%">Select</th>
              <th style="width: 40%">Name</th>
              <th style="width: 50%">Description</th>
            </tr>

            <tr v-for="workflow in dag_discriptions" :key="workflow">
              <td>
                <input
                  type="radio"
                  :id="workflow.name"
                  name="workflow.name"
                  :value="workflow.name"
                  @change="radioClick"
                />
              </td>
              <td>{{ workflow.name }}</td>
              <td>{{ workflow.description }}</td>
            </tr>
          </table>
        </div>
        <p v-if="dataMissing" id="dataMissingTag">Please select an entry!</p>
      </el-form>

      <el-form v-if="active === 1">
        <div class="stepper-form" id="fileSelect">
          <input
            class="searchInput"
            type="text"
            id="rawFilesInput"
            @keyup="searchRawFiles"
            placeholder="&#x1F50D; Search for raw Files..."
          />
          <table id="selectRawFileTable">
            <tr class="header">
              <th style="width: 15%">Select</th>
              <th style="width: 90%">Filename</th>
            </tr>

            <tr v-for="rawFile in raw_files" :key="rawFile">
              <td>
                <input
                  type="radio"
                  :id="rawFile"
                  name="workflow.name"
                  :value="rawFile"
                  @change="radioRawFileClick"
                />
              </td>
              <td>{{ rawFile }}</td>
            </tr>
          </table>
        </div>
        <p v-if="dataMissing" id="dataMissingTag">Please select an entry!</p>
      </el-form>

      <el-form v-if="active === 2">
        <div class="stepper-form" id="checkSubmit">
          <p><b>Are the following attributes correct?</b></p>
          <p>Workflow: {{ radioDataWorkflow }}</p>
          <p>File: {{ radioRawFile }}</p>
        </div>
      </el-form>
    </div>

    <div
      v-if="!isDataLoaded"
      v-loading="loading"
      element-loading-background="rgba(122, 122, 122, 0.0)"
      class="stepper-form"
    ></div>

    <el-button
      id="nextButton"
      type="primary"
      style="margin-top: 12px"
      @click="next"
      >Next step</el-button
    >
  </div>
</template>

<script setup>
import { onBeforeMount, ref } from "vue";
import { onMounted } from "vue";
import { Search } from "@element-plus/icons-vue";

import axios from "axios";
//const active = ref(0)
const dag_ids = [];
const radio1 = ref("1");
const radio_data = ref("");

const input1 = ref("");
</script>

<script>
import { ElNotification } from "element-plus";
import { ElMessage, ElMessageBox } from "element-plus";

export default {
  data() {
    return {
      isDataLoaded: false,
      dag_ids: [],
      dag_discriptions: [],
      raw_files: [],
      loading: true,
      radioDataWorkflow: "",
      radioRawFile: "",
      dataMissing: false,
      dag_run_id: "",
      active: 0,
    };
  },

  methods: {
    searchRawFiles() {
      var input, filter, table, tr, td, i, txtValue;
      input = document.getElementById("rawFilesInput");
      filter = input.value.toUpperCase();
      table = document.getElementById("selectRawFileTable");
      tr = table.getElementsByTagName("tr");

      for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[1];
        if (td) {
          txtValue = td.textContent || td.innerText;
          if (txtValue.toUpperCase().indexOf(filter) > -1) {
            tr[i].style.display = "";
          } else {
            tr[i].style.display = "none";
          }
        }
      }
    },

    searchWorkflows() {
      var input, filter, table, tr, td, i, txtValue;
      input = document.getElementById("myInput");
      filter = input.value.toUpperCase();
      table = document.getElementById("selectWorkflowTable");
      tr = table.getElementsByTagName("tr");

      for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[1];
        if (td) {
          txtValue = td.textContent || td.innerText;
          if (txtValue.toUpperCase().indexOf(filter) > -1) {
            tr[i].style.display = "";
          } else {
            tr[i].style.display = "none";
          }
        }
      }
    },

    next() {
      if (this.active == 0 && this.radioDataWorkflow == "") {
        document.getElementById("fileSelect").style.borderColor = "red";
        this.dataMissing = true;
      } else if (this.active == 0 && this.radioDataWorkflow != "") {
        this.active++;
      } else if (this.active == 1 && this.radioRawFile == "") {
        document.getElementById("fileSelect").style.borderColor = "red";
        this.dataMissing = true;
      } else if (this.active == 1 && this.radioRawFile != "") {
        this.active++;
        document.getElementById("nextButton").innerText = "Submit";
      } else if (this.active == 2) {
        this.active++;
        this.submitWorkflow();
        document.getElementById("nextButton").style.display = "none";
      }
    },

    radioClick(radioData) {
      this.radioDataWorkflow = radioData.target.id;
      document.getElementById("fileSelect").style.borderColor = "lightgrey";
      this.dataMissing = false;
    },

    radioRawFileClick(radioData) {
      this.radioRawFile = radioData.target.id;
      document.getElementById("fileSelect").style.borderColor = "lightgrey";
      this.dataMissing = false;
    },

    sleep(milliseconds) {
      return new Promise((resolve) => setTimeout(resolve, milliseconds));
    },

    async doRequests() {
      await axios
        .get(this.$airflowApi + "/api/v1/dags", {
          auth: {
            username: "airflow",
            password: "airflow",
          },
          withCredentials: true,
        })
        .then((response) => {
          for (var index in response.data["dags"]) {
            this.dag_ids.push(response.data["dags"][index]["dag_id"]);
            this.dag_discriptions.push({
              name: response.data["dags"][index]["dag_id"],
              description: response.data["dags"][index]["description"],
            });
          }
        });

      await axios.get(this.$frontendApi + "/getData", {}).then((response) => {
        for (var index in response.data["files"]) {
          this.raw_files.push(response.data["files"][index]);
        }
      });

      await this.sleep(5000);
      this.isDataLoaded = true;
    },

    submitWorkflow() {
      axios
        .post(
          this.$airflowApi +
            "/api/v1/dags/" +
            this.radioDataWorkflow +
            "/dagRuns",
          { conf: { file: this.radioRawFile } },
          {
            auth: {
              username: "airflow",
              password: "airflow",
            },
          }
        )
        .then((response) => {
          this.dag_run_id = response.data.dag_run_id;
        });

      ElNotification({
        title: "Success",
        message: "Successfully submitted Workflow!",
        type: "success",
        position: "bottom-right",
      });

      ElMessageBox.confirm(
        "Continue with detailed view?",
        "Successfully submitted workflow",
        {
          confirmButtonText: "Yes",
          cancelButtonText: "No",
          type: "info",
        }
      )
        .then(() => {
          this.$router.push(
            "/WorkflowDetails?dagRunId=" +
              this.dag_run_id +
              "&dagId=" +
              this.radioDataWorkflow +
              "&file=" +
              this.radioRawFile
          );
        })
        .catch(() => {
          ElMessage({
            type: "info",
            message: "Delete canceled",
          });
        });
    },
  },

  created() {
    this.doRequests();
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

.stepper-form {
  width: 80%;
  border: 2px lightgrey;
  border-style: solid;
  border-radius: 10px;
  min-height: 200px;
  padding: 0.5%;
}
th {
  text-align: left;
}

#dataMissingTag {
  color: red;
}

#checkSubmit {
  text-align: center;
  vertical-align: middle;
  padding: 70px 0;
}
</style>