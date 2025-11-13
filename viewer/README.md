# Forum Viewer

A TypeScript + React + Vite project with Chakra UI for viewing forum data.

## Prerequisites

Before you can run this project, you need to have Node.js and npm installed on your system.

### Installing Node.js

You can install Node.js in several ways:

#### Option 1: Using nvm (Recommended)
```bash
# Install nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# Restart your terminal or run:
source ~/.bashrc

# Install Node.js (LTS version)
nvm install --lts
nvm use --lts
```

#### Option 2: Using package manager (Fedora/RHEL-based systems)
```bash
sudo dnf install nodejs npm
```

## Setup

Once Node.js is installed, run:

```bash
npm install
```

## Development

To start the development server:

```bash
npm run dev
```

The application will be available at `http://localhost:5173`

## Build

To create a production build:

```bash
npm run build
```

## Features

- ⚡️ Vite - Fast build tool and development server
- ⚛️ React 18 - Latest version of React
- 🎨 Chakra UI - Accessible and customizable component library
- 📘 TypeScript - Type safety and better developer experience
- 🎭 Emotion - Powerful CSS-in-JS library (required by Chakra UI)
- 🌈 Framer Motion - Animation library (required by Chakra UI)

## Project Structure

```
viewer/
├── src/
│   ├── App.tsx          # Main application component
│   ├── main.tsx         # Application entry point with ChakraProvider
│   ├── index.css        # Global styles
│   └── vite-env.d.ts    # Vite type definitions
├── index.html           # HTML entry point
├── package.json         # Project dependencies and scripts
├── tsconfig.json        # TypeScript configuration
├── tsconfig.node.json   # TypeScript config for Node
└── vite.config.ts       # Vite configuration
```

