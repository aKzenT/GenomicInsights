import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify'
import { loadFonts } from './plugins/webfontloader'
import 'vuetify/dist/vuetify.min.css'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

loadFonts()


const app = createApp(App)
  .use(vuetify)
  .use(ElementPlus)



const rootComponent = app
  .use(router)
  .mount("#app");



app.config.globalProperties.$frontendApi = 'http://localhost:5000';
app.config.globalProperties.$airflowApi = 'http://localhost:8080';

