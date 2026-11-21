import { useCallback, useEffect, useMemo, useState } from 'react'
import { applyNodeChanges, Background, BaseEdge, ConnectionMode, ReactFlow, useReactFlow } from '@xyflow/react'
import type { Edge, EdgeProps, Node, NodeChange } from '@xyflow/react'
import { DeviceNode } from './DeviceNode'
import { ComponentShelf } from './ComponentShelf'
import type { CanvasNode } from './DeviceNode'
import { assets, changeWire, devices, exportWorkspace, importWorkspace, initialPositions, pinHitSize, terminalKey } from './model'
import type { Device, Pin, PositionMap, Registry, Terminal, Wire } from './model'

const nodeTypes = { part: DeviceNode }
type WireEdge = Edge<{ inspected: boolean }, 'wire'>
function wireTangent(device: string, pin: string | null | undefined): [number, number] {
  if (device === 'board') return [pin?.startsWith('J2.') ? -1 : 1, 0]
  if (device === 'resistor') return [pin === '1' ? -1 : 1, 0]
  return [0, 1]
}
function WirePath({ id, source, target, sourceHandleId, targetHandleId, sourceX, sourceY, targetX, targetY, data }: EdgeProps<WireEdge>) {
  // Flow reports the left edge for Position.Left handles.
  sourceX += pinHitSize / 2
  targetX += pinHitSize / 2
  const turn = Math.max(32, Math.hypot(targetX - sourceX, targetY - sourceY) * .42)
  const [sx, sy] = wireTangent(source, sourceHandleId)
  const [tx, ty] = wireTangent(target, targetHandleId)
  const path = ['M', sourceX, sourceY, 'C', sourceX + sx * turn, sourceY + sy * turn, targetX + tx * turn, targetY + ty * turn, targetX, targetY].join(' ')
  return <BaseEdge id={id} path={path} interactionWidth={15}
    style={{ stroke: data?.inspected ? '#8bf1dc' : '#54bda9', strokeWidth: data?.inspected ? 3.5 : 2.5 }} />
}
const edgeTypes = { wire: WirePath }
const initialHistory = { past: [] as Wire[][], present: [] as Wire[], future: [] as Wire[][] }
type LayoutNode = Node<{ device: Device }, 'part'>
const initialLayout: LayoutNode[] = devices.map(device => ({
  id: device, type: 'part', position: initialPositions[device], dragHandle: '.drag-part', selectable: false, data: { device },
}))

export function Workspace({ entry }: { entry: boolean }) {
  const [layout, setLayout] = useState(() => entry ? [] : initialLayout)
  const [registry, setRegistry] = useState<Registry>({})
  const [errors, setErrors] = useState<Partial<Record<Device, string>>>({})
  const [history, setHistory] = useState(initialHistory)
  const [draft, setDraft] = useState<{ from: Terminal; rewire?: string }>()
  const [inspected, inspect] = useState<Terminal>()
  const [selected, select] = useState('')
  const [message, setMessage] = useState('')
  const [transfer, setTransfer] = useState('')
  const [locator, setLocator] = useState('')
  const [actualZoom, setActualZoom] = useState(1)
  const flow = useReactFlow<CanvasNode, WireEdge>()
  const wires = history.present
  const selectedWire = wires.find(wire => wire.id === selected)
  const livePin = (ref: Terminal) => registry[ref.instanceId]?.some(pin => pin.id === ref.visualPinId)

  const placePart = (device: Device) => {
    if (!entry || device === 'board') return
    const part = initialLayout.find(node => node.id === device)
    if (part) setLayout(current => current.some(node => node.id === part.id) ? current : [...current, part])
  }

  const onPins = useCallback((device: Device, pins: Pin[] | null, error?: string) => {
    setRegistry(previous => ({ ...previous, [device]: pins ?? undefined }))
    setErrors(previous => ({ ...previous, [device]: error }))
    if (!pins) setDraft(current => current?.from.instanceId === device ? undefined : current)
  }, [])
  const commit = (next: Wire[]) => setHistory(current => ({ past: [...current.past, current.present], present: next, future: [] }))
  const cancel = () => { setDraft(undefined); setMessage('Draft canceled.') }
  const undo = () => {
    setDraft(undefined)
    setHistory(({ past, present, future }) => past.length
      ? { past: past.slice(0, -1), present: past.at(-1)!, future: [present, ...future] } : { past, present, future })
  }
  const redo = () => {
    setDraft(undefined)
    setHistory(({ past, present, future }) => future.length
      ? { past: [...past, present], present: future[0], future: future.slice(1) } : { past, present, future })
  }
  const remove = () => {
    if (!selectedWire) return
    commit(wires.filter(wire => wire.id !== selectedWire.id))
    setDraft(undefined)
    setMessage('Wire deleted.')
  }
  const selectPin = (pin: Terminal) => {
    inspect(pin)
    setMessage('')
    if (!livePin(pin)) return setMessage('Pin unavailable.')
    if (!draft) return setDraft({ from: pin })
    try {
      const next = changeWire(wires, draft.from, pin, registry, draft.rewire)
      commit(next)
      select(draft.rewire ?? next.at(-1)!.id)
      setDraft(undefined)
      setMessage(entry ? 'Visual wire connected.' : 'Visual wire saved.')
    } catch (error) { setMessage((error as Error).message) }
  }
  const beginRewire = () => {
    if (selectedWire && livePin(selectedWire.a)) {
      setDraft({ from: selectedWire.a, rewire: selectedWire.id })
      setMessage('Select a replacement destination.')
    }
  }
  const copyOut = () => {
    if (wires.some(wire => !livePin(wire.a) || !livePin(wire.b))) return setMessage('A wire references a contact that is unavailable.')
    const positions = Object.fromEntries(layout.map(node => [node.id, node.position])) as PositionMap
    setTransfer(exportWorkspace(positions, wires))
    setMessage('Visual JSON ready.')
  }
  const load = () => {
    try {
      const next = importWorkspace(transfer, registry)
      setLayout(current => current.map(node => ({ ...node, position: next.positions[node.data.device] })))
      setHistory({ ...initialHistory, present: next.wires })
      select('')
      setDraft(undefined)
      setMessage('Visual workspace loaded.')
    } catch (error) {
      setMessage('Import rejected. ' + (error as Error).message)
    }
  }

  useEffect(() => {
    const hotkeys = (event: KeyboardEvent) => {
      if (entry && document.querySelector('dialog[open]')) return
      if (event.key === 'Escape' && draft) { event.preventDefault(); cancel(); return }
      if ((event.target as HTMLElement | null)?.closest('input, textarea, select, [contenteditable]')) return
      if (event.key === 'Delete' && selectedWire) { event.preventDefault(); remove() }
      if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === 'z') {
        event.preventDefault()
        if (event.shiftKey) redo()
        else undo()
      }
    }
    window.addEventListener('keydown', hotkeys)
    return () => window.removeEventListener('keydown', hotkeys)
  })

  const nodes: CanvasNode[] = layout.map(node => ({
    ...node,
    data: {
      device: node.data.device, draft: draft ? terminalKey(draft.from) : '', selected: inspected ? terminalKey(inspected) : '',
      onPins, onPin: selectPin, onInspect: inspect,
    },
  }))
  const edges: WireEdge[] = wires.filter(wire => livePin(wire.a) && livePin(wire.b)).map(wire => ({
    id: wire.id, type: 'wire', source: wire.a.instanceId, sourceHandle: wire.a.visualPinId,
    target: wire.b.instanceId, targetHandle: wire.b.visualPinId, data: { inspected: selected === wire.id },
    ariaLabel: terminalKey(wire.a) + ' to ' + terminalKey(wire.b),
  }))
  const moveNodes = useCallback((changes: NodeChange<CanvasNode>[]) => {
    setLayout(previous => applyNodeChanges(changes.filter(change => change.type === 'position' || change.type === 'dimensions'), previous))
  }, [])
  const pinOptions = useMemo(() => devices.flatMap(device => (registry[device] ?? []).map(pin => device + '/' + pin.id)), [registry])
  const locate = () => {
    const target = Array.from(document.querySelectorAll<HTMLElement>('[data-terminal]'))
      .find(handle => handle.dataset.terminal === locator)
    if (!target) return
    const point = target.getBoundingClientRect()
    const position = flow.screenToFlowPosition({ x: point.x + point.width / 2, y: point.y + point.height / 2 })
    void flow.setCenter(position.x, position.y, { zoom: Math.max(actualZoom, 1) })
    target.focus({ preventScroll: true })
  }

  return <main className="workspace">
    <header className="topbar">
      {entry ? <>
        <h1 className="entry-heading" lang="ka">INVENTOR EDU — ვიზუალური ექსპერიმენტი</h1>
        <ComponentShelf placed={new Set(layout.map(node => node.data.device))} onPlace={placePart} />
      </> : <div className="brand"><span className="brand-mark" aria-hidden="true">⟐</span><div><strong>Inventor EDU</strong><small>Component workspace</small></div></div>}
      <div className="toolbar" aria-label="Editing tools">
        <button type="button" disabled={!history.past.length} onClick={undo}>↶ Undo</button>
        <button type="button" disabled={!history.future.length} onClick={redo}>↷ Redo</button>
        <button type="button" onClick={() => { void flow.fitView({ padding: .35, maxZoom: 1 }) }}>Fit view</button>
      </div>
      {!entry && <div className="mode"><span/> Visual only</div>}
    </header>
    <div className="content">
      <section className="viewport" aria-label="Circuit canvas">
        <ReactFlow<CanvasNode, WireEdge> nodes={nodes} edges={edges} nodeTypes={nodeTypes} edgeTypes={edgeTypes}
          connectionMode={ConnectionMode.Loose} onNodesChange={moveNodes}
          onEdgeClick={(_event, edge) => { select(edge.id); setMessage('') }}
          onMove={(_event, viewport) => setActualZoom(viewport.zoom)}
          onInit={instance => { void instance.setCenter(421, 252, { zoom: 1 }) }}
          minZoom={.15} maxZoom={3} deleteKeyCode={null} nodesConnectable={false} connectOnClick={false} panOnDrag
          nodesFocusable={false} edgesFocusable={false} panActivationKeyCode={null} zoomOnDoubleClick={false}
          translateExtent={[[-10000, -10000], [10000, 10000]]}
          nodeExtent={[[-10000, -10000], [10000, 10000]]}
          colorMode="dark">
          <Background gap={19} size={1} color="#3b4850" />
        </ReactFlow>
        <div className="canvas-title"><span/> Circuit canvas</div>
        <div className="zoom-control" aria-label="Canvas zoom">
          {[.5, 1, 2].map(zoom => <button type="button" key={zoom} aria-label={'Zoom ' + zoom + 'x'}
            aria-pressed={Math.abs(actualZoom - zoom) < .001}
            onClick={() => { void flow.zoomTo(zoom) }}>{zoom}×</button>)}
          <output aria-label="Current zoom">{Math.round(actualZoom * 100)}%</output>
        </div>
      </section>
      <aside className="inspector" aria-label="Workspace inspector">
        {entry ? <h2>Inspector</h2> : <h1>Inspector</h1>}
        {entry && layout.length === 0 && <p lang="ka">კომპონენტები ჯერ არ არის დამატებული</p>}
        <section>
          <h2>Contact</h2>
          <label htmlFor="pin-locator">Find a physical contact</label>
          <div className="locator">
            <select id="pin-locator" value={locator} onChange={event => setLocator(event.target.value)}>
              <option value="">Select contact</option>
              {pinOptions.map(key => <option key={key}>{key}</option>)}
            </select>
            <button type="button" disabled={!locator} onClick={locate}>Focus</button>
          </div>
          {inspected ? <div className="contact-readout">
            <strong>{terminalKey(inspected)}</strong>
            <small>{livePin(inspected) ? 'VISUAL_PIN_AVAILABLE' : 'VISUAL_PIN_UNAVAILABLE'}</small>
            <small>CANONICAL_MAPPING_UNAVAILABLE</small>
          </div> : entry ? <p lang="ka">კონტაქტი არ არის არჩეული</p> :
            <p>Hover a pin or find it by its physical ID.</p>}
        </section>
        <section>
          <h2>Wires <span className="count">{wires.length}</span></h2>
          <p className="draft" aria-live="polite">{draft ? 'From ' + terminalKey(draft.from) + ' · choose destination' : 'Select two contacts to draw a wire.'}</p>
          {draft && <button type="button" onClick={cancel}>Cancel draft</button>}
          <ul className="wire-list">
            {wires.map(wire => <li key={wire.id}><button type="button" aria-pressed={selected === wire.id}
              onClick={() => select(wire.id)}>
              {terminalKey(wire.a)} <span aria-hidden="true">→</span> {terminalKey(wire.b)}
            </button></li>)}
          </ul>
          {selectedWire && <div className="wire-actions">
            <button type="button" onClick={beginRewire}>Rewire destination</button>
            <button type="button" onClick={remove}>Delete wire</button>
          </div>}
        </section>
        {!entry && <details className="transfer">
          <summary>Visual workspace JSON</summary>
          <label htmlFor="workspace-json">Workspace data</label>
          <textarea id="workspace-json" spellCheck={false} value={transfer} onChange={event => setTransfer(event.target.value)} />
          <div className="wire-actions"><button type="button" onClick={copyOut}>Export</button><button type="button" onClick={load}>Import</button></div>
        </details>}
        <details className="provenance">
          <summary>Asset provenance</summary>
          {!entry && <p>Innerscene CC0 nominal ESP32-DevKitC V4 CAD. Exact ESP32-WROOM-32E fit is pending. Contact names follow Espressif header order.</p>}
          <p>HC-SR04, LED and resistor by Wokwi Elements 1.9.2 (MIT).</p>
        </details>
        {Object.entries(errors).filter(([, error]) => error).map(([device, error]) => <p key={device} role="alert">{assets[device as Device].name}: {error}</p>)}
      </aside>
    </div>
    <footer className="statusbar">
      <strong>{entry ? 'VISUAL_ONLY_NOT_ENGINEERING_VERIFIED' : 'NOT_ENGINEERING_VERIFIED'}</strong>
      {entry && <span>TEST_ONLY · SEMANTIC_EXPERIMENT_NOT_VISUAL_DESIGN</span>}
      <span role="status">{message || 'No electrical or firmware simulation.'}</span>
      <span className="status-shortcuts">Enter select · Esc cancel · Del remove</span>
    </footer>
  </main>
}
