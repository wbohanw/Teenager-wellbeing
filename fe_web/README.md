# Milo - Teenager Wellbeing App

A React application built with TypeScript and Tailwind CSS, designed to provide an AI-powered mental health companion for teenagers.

## Tech Stack

- React
- TypeScript
- Tailwind CSS
- Vite

## Getting Started

### Prerequisites

- Node.js (v14.0.0 or higher)
- npm or yarn

### Installation

1. Clone the repository
2. Install dependencies:

```bash
cd fe_web
npm install
# or with yarn
yarn
```

3. Install Tailwind CSS and its dependencies:

```bash
npm install -D tailwindcss postcss autoprefixer
# or with yarn
yarn add -D tailwindcss postcss autoprefixer
```

4. Run the development server:

```bash
npm run dev
# or with yarn
yarn dev
```

## Project Structure

```
fe_web/
├── public/             # Static assets
├── src/
│   ├── ChatPage/       # Chat interface components
│   ├── LandingPage/    # Landing page components
│   ├── Preferences/    # User preferences components
│   ├── images/         # Image assets
│   ├── videos/         # Video assets
│   ├── App.tsx         # Main App component
│   ├── connector.ts    # API connection utilities
│   ├── index.css       # Global styles with Tailwind directives
│   └── index.tsx       # Entry point
├── tailwind.config.js  # Tailwind configuration
├── postcss.config.js   # PostCSS configuration
└── vite.config.ts      # Vite configuration
```

## Features

- Chat interface with animated character responses
- User preferences customization
- Dark/light mode toggle
- Responsive design for all screen sizes

# React + TypeScript + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## Expanding the ESLint configuration

If you are developing a production application, we recommend updating the configuration to enable type-aware lint rules:

```js
export default tseslint.config({
  extends: [
    // Remove ...tseslint.configs.recommended and replace with this
    ...tseslint.configs.recommendedTypeChecked,
    // Alternatively, use this for stricter rules
    ...tseslint.configs.strictTypeChecked,
    // Optionally, add this for stylistic rules
    ...tseslint.configs.stylisticTypeChecked,
  ],
  languageOptions: {
    // other options...
    parserOptions: {
      project: ['./tsconfig.node.json', './tsconfig.app.json'],
      tsconfigRootDir: import.meta.dirname,
    },
  },
})
```

You can also install [eslint-plugin-react-x](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-x) and [eslint-plugin-react-dom](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-dom) for React-specific lint rules:

```js
// eslint.config.js
import reactX from 'eslint-plugin-react-x'
import reactDom from 'eslint-plugin-react-dom'

export default tseslint.config({
  plugins: {
    // Add the react-x and react-dom plugins
    'react-x': reactX,
    'react-dom': reactDom,
  },
  rules: {
    // other rules...
    // Enable its recommended typescript rules
    ...reactX.configs['recommended-typescript'].rules,
    ...reactDom.configs.recommended.rules,
  },
})
```
