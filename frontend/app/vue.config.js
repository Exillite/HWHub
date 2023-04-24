const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
    transpileDependencies: true,
    devServer: { allowedHosts: 'all', },
    pluginOptions: {
      moment: {
        locales: [
          ''
        ]
      },
      vuetify: {},
      i18n: {
        locale: 'ru',
        fallbackLocale: 'ru',
        localeDir: 'locales',
        enableLegacy: false,
        runtimeOnly: false,
        compositionOnly: false,
        fullInstall: true
      }
    }
})
