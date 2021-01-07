
const path = require('path')
const BundleTracker = require("webpack-bundle-tracker");

module.exports = {
  publicPath: "http://0.0.0.0:8080/",
  outputDir: "./dist/",
  chainWebpack: (config) => {
    config.outputDir = path.resolve(__dirname, "../static");
    config.publicPath = '/static/';
    config.output.filename("[name].js");
    config.output.chunkFilename("[id]-[chunkhash].js");

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
          path.resolve(__dirname, 'node_modules')
        ]
      })
      .https(false)
      .disableHostCheck(true)
      .headers({ "Access-Control-Allow-Origin": ["*"] });
    config.devServer.writeToDisk = true
  },
  css: {
    // Enable CSS source maps.
    sourceMap: process.env.NODE_ENV !== 'production'
  }
};
