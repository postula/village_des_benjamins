module.exports = {
    extends: [
        // add more generic rulesets here, such as:
        'eslint:recommended',
        'plugin:vue/vue3-recommended',
        // 'plugin:vue/recommended' // Use this if you are using Vue.js 2.x.
    ],
    rules: {
        // override/add rules settings here, such as:
        // 'vue/no-unused-vars': 'error'
    },
    parserOptions: {
        parser: 'babel-eslint',
        ecmaVersion: 6
    },
}
