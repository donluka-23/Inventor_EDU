import { createRoot } from 'react-dom/client'
import { ReactFlowProvider } from '@xyflow/react'
import { Workspace } from './Workspace'
import '@xyflow/react/dist/style.css'
import './style.css'

const entry = window.location.pathname === '/' && window.location.search === '?ux=entry'
createRoot(document.getElementById('root')!).render(<ReactFlowProvider><Workspace entry={entry} /></ReactFlowProvider>)
