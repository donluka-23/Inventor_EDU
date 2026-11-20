import { createElement, useEffect, useRef, useState } from 'react'
import { Handle, Position, useUpdateNodeInternals } from '@xyflow/react'
import type { Node, NodeProps } from '@xyflow/react'
import '@wokwi/elements/dist/esm/hc-sr04-element.js'
import '@wokwi/elements/dist/esm/led-element.js'
import '@wokwi/elements/dist/esm/resistor-element.js'
import boardImage from './assets/devkitc-v4.png'
import boardSource from './assets/devkitc-v4.json?raw'
import { assets, pinHitSize, terminalKey, validatePins } from './model'
import type { Device, Pin, Terminal } from './model'

const boardWidth = 150
const boardHeight = boardWidth * 51 / 29
const library = {
  sensor: { tag: 'wokwi-hc-sr04', scale: 1.52, width: 259, height: 150 },
  led: { tag: 'wokwi-led', scale: 1.65, width: 66, height: 83 },
  resistor: { tag: 'wokwi-resistor', scale: 1.94, width: 115, height: 23 },
}
type WokwiElement = HTMLElement & {
  pinInfo?: { name: string; x: number; y: number }[]
  updateComplete?: Promise<boolean>
}
type DeviceData = {
  device: Device
  draft: string
  selected: string
  onPins: (device: Device, pins: Pin[] | null, error?: string) => void
  onPin: (terminal: Terminal) => void
  onInspect: (terminal: Terminal) => void
}
export type CanvasNode = Node<DeviceData, 'part'>

async function digest(bytes: ArrayBuffer) {
  const hash = await crypto.subtle.digest('SHA-256', bytes)
  return 'sha256:' + Array.from(new Uint8Array(hash), byte => byte.toString(16).padStart(2, '0')).join('')
}

let geometry: Promise<Pin[]> | undefined
function verifiedBoardGeometry() {
  return geometry ??= (async () => {
    const response = await fetch(boardImage)
    if (!response.ok) throw Error('Board image unavailable')
    const imageHash = await digest(await response.arrayBuffer())
    const geometryHash = await digest(new TextEncoder().encode(boardSource).buffer)
    if (imageHash + '+' + geometryHash !== assets.board.revision) throw Error('Board asset digest mismatch')
    const data = JSON.parse(boardSource)
    if (data.width !== 29 || data.height !== 51 || !Array.isArray(data.pins)) throw Error('Unsupported board geometry')
    return validatePins('board', data.pins.map((pin: Pin) => ({
      id: pin.id, x: pin.x * boardWidth, y: pin.y * boardHeight,
    })), boardWidth, boardHeight)
  })()
}

export function DeviceNode({ id, data }: NodeProps<CanvasNode>) {
  const { device, onPins } = data
  const host = useRef<WokwiElement>(null)
  const image = useRef<HTMLImageElement>(null)
  const [pins, setPins] = useState<Pin[]>([])
  const updateInternals = useUpdateNodeInternals()
  const spec = device === 'board' ? { scale: 1, width: boardWidth, height: boardHeight } : library[device]

  useEffect(() => {
    let active = true
    let generation = 0
    const publish = (next: Pin[] | null, error?: string) => {
      if (!active) return
      setPins(next ?? [])
      onPins(device, next, error)
    }
    if (device === 'board') {
      const assetImage = image.current!
      verifiedBoardGeometry().then(async next => {
        await assetImage.decode()
        if (assetImage.naturalWidth !== 580 || assetImage.naturalHeight !== 1020) throw Error('Unexpected board image size')
        publish(next)
      }).catch(error => publish(null, String(error)))
      return () => { active = false }
    }

    const element = host.current!
    const refresh = async () => {
      const current = ++generation
      try {
        await element.updateComplete
        if (!active || current !== generation) return
        const svg = element.shadowRoot?.querySelector('svg')
        const raw = element.pinInfo
        if (!svg || !Array.isArray(raw) || !svg.getBoundingClientRect().width) throw Error('Renderer pinInfo unavailable')
        if (raw.some(pin => !pin || !Number.isFinite(pin.x) || !Number.isFinite(pin.y))) throw Error('Invalid renderer pinInfo')
        // The upstream API uses native CSS px. Local CSS scale precedes the
        // React Flow viewport transform. getBoundingClientRect includes both.
        const width = Number.parseFloat(getComputedStyle(svg).width) * spec.scale
        const height = Number.parseFloat(getComputedStyle(svg).height) * spec.scale
        publish(validatePins(device, raw.map(({ name, x, y }) => ({
          id: name, x: x * spec.scale, y: y * spec.scale,
        })), width + .1, height + .1))
      } catch (error) {
        if (current === generation) publish(null, String(error))
      }
    }
    const resize = new ResizeObserver(() => { void refresh() })
    const mutation = new MutationObserver(() => { void refresh() })
    resize.observe(element)
    mutation.observe(element, { attributes: true })
    if (element.shadowRoot) mutation.observe(element.shadowRoot, { attributes: true, subtree: true, childList: true })
    void refresh()
    return () => {
      active = false
      resize.disconnect()
      mutation.disconnect()
    }
  }, [device, onPins, spec.scale])

  useEffect(() => { updateInternals(id) }, [id, pins, updateInternals])

  return <div className={'part part-' + device} data-device={device}
    style={{ width: spec.width, height: spec.height }}>
    <header className="part-label drag-part">
      {assets[device].name}
      {device === 'board' && <small>Nominal CAD · WROOM-32E fit pending</small>}
    </header>
    {device === 'board'
      ? <img ref={image} className="board-image drag-part" src={boardImage} alt="Nominal DevKitC V4 CAD, USB at bottom"
          style={{ visibility: pins.length ? 'visible' : 'hidden' }} draggable={false} />
      : <div className="library-art drag-part" style={{ transform: 'scale(' + spec.scale + ')' }}>
          {createElement(library[device].tag, { ref: host })}
        </div>}
    {device === 'board' && <div className="header-labels" aria-hidden="true"><span>J2</span><span>J3</span></div>}
    {pins.map(pin => {
      const terminal = { instanceId: device, visualPinId: pin.id }
      const key = terminalKey(terminal)
      return <Handle key={key} id={pin.id} type="source" position={Position.Left}
        className={'visual-pin nodrag nopan' + (data.draft === key || data.selected === key ? ' marked' : '')}
        aria-label={key} aria-pressed={data.draft === key || data.selected === key}
        title={key} tabIndex={0} role="button" data-terminal={key}
        isConnectable={false} isConnectableStart={false} isConnectableEnd={false}
        style={{ left: pin.x, top: pin.y, width: pinHitSize, height: pinHitSize }}
        onPointerEnter={() => data.onInspect(terminal)} onFocus={() => data.onInspect(terminal)}
        onPointerDownCapture={event => {
          if (!event.isPrimary || event.button !== 0) return
          event.preventDefault()
          event.stopPropagation()
          event.currentTarget.focus({ preventScroll: true })
          data.onPin(terminal)
        }}
        onClick={event => {
          event.stopPropagation()
          if (event.detail === 0) data.onPin(terminal)
        }}
        onKeyDown={event => {
          if (event.key === 'Enter' || event.key === ' ') {
            event.preventDefault()
            event.stopPropagation()
            data.onPin(terminal)
          }
        }}>
        <span className="pin-caption" aria-hidden="true">{pin.id}</span>
      </Handle>
    })}
  </div>
}
