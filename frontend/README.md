# AI Contract Intelligence & Risk Scoring Platform - Frontend

This is the React + Vite frontend dashboard for the **AI Contract Intelligence & Risk Scoring Platform**. It has been designed with custom corporate style tokens and features full mock simulation capabilities alongside direct FastAPI integration bindings.

---

## 🎨 Design Tokens & Theme Configuration
The application leverages the following custom brand color tokens (defined in `tailwind.config.js`):
*   **Primary Slate / Text Headers**: `brand-slate` (`#326273`)
*   **Primary Light / Brand Accents**: `brand-blue` (`#5C9EAD`)
*   **Background Canvas**: `brand-platinum` (`#EEEEEE`)
*   **Clean Spaces / Cards**: `brand-white` (`#FFFFFF`)
*   **Risk Alerts / Accents**: `brand-tangerine` (`#E39774`)

---

## 🚀 Local Quickstart Guide

### 1. Prerequisites
Ensure you have [Node.js](https://nodejs.org/) installed (v18+ recommended).

### 2. Install Dependencies
Navigate into the `frontend` folder and run the installation command:
```bash
cd frontend
npm install
```

### 3. Start Development Server
Run the local Vite dev server:
```bash
npm run dev
```
Open your browser and navigate to: [http://localhost:3000](http://localhost:3000)

### 4. Build for Production
Verify that compilation compiles correctly and builds optimized assets:
```bash
npm run build
```

---

## 🔗 FastAPI Backend Integration
By default, the platform runs in **Mock Mode Active** so you can preview files instantly without running a backend.
To connect to your real FastAPI backend:
1. Click the **Settings Gear Icon** in the top right corner.
2. Enter your running FastAPI server endpoint (e.g. `http://localhost:8000`).
3. Click **Test Connection** to check connectivity (CORS must be enabled in FastAPI).
4. Click **Save Changes**.
5. Click **Mock Mode Active** in the header to toggle it to **Live API Integration**.
6. Upload a contract PDF file. The frontend will hit `/upload`, `/analyze`, `/entities`, and `/classify-clause` endpoints sequentially.

---

## ⚡ Deployment to Vercel

You can deploy the app to Vercel instantly using the Vercel CLI.

### 1. Install Vercel CLI Globally
```bash
npm install -g vercel
```

### 2. Login to Vercel
```bash
vercel login
```

### 3. Deploy
Run the command in the `frontend` folder to trigger a preview deployment:
```bash
vercel
```
To deploy directly to production:
```bash
vercel --prod
```
The preconfigured [vercel.json](file:///d:/btech/Zaalima_dev_pvt.ltd/AI-Contract-Intelligence_2-main/AI-Contract-Intelligence_2-main/frontend/vercel.json) file handles routing redirects automatically, ensuring React routes load cleanly.
