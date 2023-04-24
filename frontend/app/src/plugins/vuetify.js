<<<<<<< HEAD
=======
/**
 * plugins/vuetify.js
 *
 * Framework documentation: https://vuetifyjs.com`
 */

>>>>>>> parent of 14b8c8b (Added frontend)
// Styles
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'

<<<<<<< HEAD
// Vuetify
import { createVuetify } from 'vuetify'

export default createVuetify(
  // https://vuetifyjs.com/en/introduction/why-vuetify/#feature-guides
)
=======
// Composables
import { createVuetify } from 'vuetify'

// https://vuetifyjs.com/en/introduction/why-vuetify/#feature-guides
export default createVuetify({
  theme: {
    themes: {
      light: {
        colors: {
          primary: '#1867C0',
          secondary: '#5CBBF6',
        },
      },
    },
  },
})
>>>>>>> parent of 14b8c8b (Added frontend)
