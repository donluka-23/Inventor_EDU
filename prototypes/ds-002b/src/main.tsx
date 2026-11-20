import { createRoot } from 'react-dom/client'
import { ReactFlowProvider } from '@xyflow/react'
import { Workspace } from './Workspace'
import '@xyflow/react/dist/style.css'
import './style.css'

createRoot(document.getElementById('root')!).render(<ReactFlowProvider><Workspace /></ReactFlowProvider>)
