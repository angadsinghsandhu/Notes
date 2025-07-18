import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'

// import components
import App from './assets/components/App/App.tsx'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
