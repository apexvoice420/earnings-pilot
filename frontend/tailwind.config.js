/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          light: '#323a54',
          DEFAULT: '#141727',
          dark: '#0b0d1a',
        },
        background: '#f8f9fa',
        card: '#ffffff',
      },
      backgroundImage: {
        'accent-gradient': 'linear-gradient(to right, #2152ff, #21d4fd)',
        'success-gradient': 'linear-gradient(to right, #17ad37, #98ec2d)',
        'warning-gradient': 'linear-gradient(to right, #f53939, #fbcf34)',
      },
      fontFamily: {
        sans: ['Inter', 'Open Sans', 'sans-serif'],
        headings: ['Poppins', 'Inter', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
