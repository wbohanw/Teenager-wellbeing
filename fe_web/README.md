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

