/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'brand-slate': '#326273',
        'brand-blue': '#5C9EAD',
        'brand-platinum': '#EEEEEE',
        'brand-white': '#FFFFFF',
        'brand-tangerine': '#E39774',
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
