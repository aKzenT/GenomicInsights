import { createRouter, createWebHistory } from 'vue-router'
import UploadData from '../views/UploadData.vue'
import StartAnalyse from '../views/StartAnalyse.vue'
import ActiveWorkflows from '../views/ActiveWorkflows.vue'
import WorkflowDetails from '../views/WorkflowDetails.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [

    {
      path: '/UploadData',
      name: 'upload_data',
      component: UploadData,
      alias: '/'
    },
    {
      path: '/StartAnalyse',
      name: 'Start_Analyse',
      component: StartAnalyse
    },
    {
      path: '/ActiveWorkflows',
      name: 'Active_Workflows',
      component: ActiveWorkflows
    },
    {
      path: '/WorkflowDetails',
      name: 'WorkflowDetails',
      component: WorkflowDetails
    },
  ]
})

export default router
