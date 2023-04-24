/**
 * plugins/webfontloader.js
 *
 * webfontloader documentation: https://github.com/typekit/webfontloader
 */

<<<<<<< HEAD
export async function loadFonts () {
=======
 export async function loadFonts () {
>>>>>>> parent of 14b8c8b (Added frontend)
  const webFontLoader = await import(/* webpackChunkName: "webfontloader" */'webfontloader')

  webFontLoader.load({
    google: {
      families: ['Roboto:100,300,400,500,700,900&display=swap'],
    },
  })
}
