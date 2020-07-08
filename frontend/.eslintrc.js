module.exports = {
  env: {
    browser: true,
    es2020: true,
  },
  extends: ['plugin:vue/recommended', 'plugin:prettier/recommended', 'prettier/vue'],
  parserOptions: {
    ecmaVersion: 2018,
    parser: '@typescript-eslint/parser',
    sourceType: 'module',
  },
  plugins: ['vue', '@typescript-eslint'],
  rules: {},
};
