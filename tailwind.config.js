/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html", //template at the project or root level
    "./**/templates/**/*.html" //template at the app level
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}

