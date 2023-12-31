/** @type {import('tailwindcss').Config} */

module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      borderRadius: {
        '4xl': '1.5rem',
      },
      fontFamily: {sans:['Barlow', 'sans-serif']}
    },
  },
  plugins: [require('@tailwindcss/forms')],
}