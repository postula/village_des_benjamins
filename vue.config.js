
const path = require('path')

module.exports = {
  publicPath: "/static/",
  outputDir: "./dist/",
  chainWebpack: (config) => {
    config.outputDir = path.resolve(__dirname, "../static");
    config.publicPath = '/static/';
    config.output.filename("[name].js");
    config.output.chunkFilename("[id]-[chunkhash].js");
    config.entry("app").clear().add("./frontend/main.js").end();
    config.resolve.alias.set("@", path.join(__dirname, "./frontend"))
    config.optimization.splitChunks(false);

    config.resolve.alias.set("__STATIC__", "static");
    config.devServer
      // the first 3 lines of the following code have been added to the configuration
      .public("http://127.0.0.1:8080")
      .host("127.0.0.1")
      .port(8080)
      .hotOnly(true)
      //.writeToDisk(true)
      .watchOptions({
        poll: 1000, ignored: [
          path.resolve(__dirname, 'dist'),
          path.resolve(__dirname, 'node_modules'),
          path.resolve(__dirname, 'venv'),
        ]
      })
      .https(false)
      .disableHostCheck(true)
      .headers({ "Access-Control-Allow-Origin": ["*"] });
    config.devServer.writeToDisk = true
  },
  css: {
    // Enable CSS source maps.
    sourceMap: process.env.NODE_ENV !== 'production',
    loaderOptions: {
      sass: {
        data: `
        @import "@/scss/_variables.scss";
      `
      }
    }
  }
};
