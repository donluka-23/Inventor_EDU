export type Device = 'board' | 'sensor' | 'led' | 'resistor'
export type Point = { x: number; y: number }
export type Pin = Point & { id: string }
export type Terminal = { instanceId: Device; visualPinId: string }
export type Wire = { id: string; a: Terminal; b: Terminal }
export type PositionMap = Record<Device, Point>
export type Registry = Partial<Record<Device, readonly Pin[]>>
export const pinHitSize = 11

export const devices: Device[] = ['board', 'sensor', 'led', 'resistor']
const wokwiRevision = '@wokwi/elements@1.9.2:sha512-bommouWNrBl6bQqxi8ZT/Keh1MbGpL7bl2pVf4DxbrngXw3G7iejt5XA2990q9i5tidGoxMYJxoP11Ai6xuQdg=='
export const assets = {
  board: { name: 'ESP32-DevKitC V4', variant: 'innerscene-v4-nominal-wroom', revision: 'sha256:9efc931ec7ba77f772ff381334eb9ca009b38076a4793805ce9eb47a35058896+sha256:fae65c6a77d2e6c7ffceab8fa3effe87a20c93e6af5e9cdbdd6aeda71dedad23' },
  sensor: { name: 'HC-SR04', variant: 'wokwi-hc-sr04-generic', revision: wokwiRevision },
  led: { name: 'LED', variant: 'wokwi-led', revision: wokwiRevision },
  resistor: { name: 'Resistor', variant: 'wokwi-resistor', revision: wokwiRevision },
} satisfies Record<Device, { name: string; variant: string; revision: string }>
export const expected = {
  board: ['J2', 'J3'].flatMap(row => Array.from({ length: 19 }, (_, i) => row + '.' + (i + 1))),
  sensor: ['VCC', 'TRIG', 'ECHO', 'GND'],
  led: ['A', 'C'],
  resistor: ['1', '2'],
} satisfies Record<Device, string[]>
export const initialPositions: PositionMap = {
  board: { x: 138, y: 113 },
  sensor: { x: 430, y: 157 },
  led: { x: 455, y: 369 },
  resistor: { x: 590, y: 410 },
}
export const terminalKey = (ref: Terminal) => ref.instanceId + '/' + ref.visualPinId
const pairKey = (a: Terminal, b: Terminal) => [terminalKey(a), terminalKey(b)].sort().join('~')

export function validatePins(device: Device, input: unknown, width: number, height: number): Pin[] {
  if (!Number.isFinite(width) || !Number.isFinite(height) || width <= 0 || height <= 0 ||
      !Array.isArray(input) || input.length !== expected[device].length) throw Error('Incomplete pin geometry')
  const pins = new Map<string, Pin>()
  for (const raw of input) {
    if (!raw || typeof raw.id !== 'string' || !expected[device].includes(raw.id) || pins.has(raw.id) ||
        !Number.isFinite(raw.x) || !Number.isFinite(raw.y) ||
        raw.x < 0 || raw.x > width || raw.y < 0 || raw.y > height ||
        [...pins.values()].some(pin => Math.hypot(pin.x - raw.x, pin.y - raw.y) < pinHitSize)) {
      throw Error('Invalid or overlapping pin geometry')
    }
    pins.set(raw.id, { id: raw.id, x: raw.x, y: raw.y })
  }
  return expected[device].map(id => pins.get(id)!)
}

export function changeWire(wires: Wire[], a: Terminal, b: Terminal, registry: Registry, rewire?: string): Wire[] {
  if (!hasPin(registry, a) || !hasPin(registry, b)) throw Error('Pin unavailable')
  if (terminalKey(a) === terminalKey(b)) throw Error('Choose two different contacts')
  if (rewire && !wires.some(wire => wire.id === rewire)) throw Error('Wire unavailable')
  if (wires.some(wire => wire.id !== rewire && pairKey(wire.a, wire.b) === pairKey(a, b))) throw Error('Wire already exists')
  let number = 1
  while (!rewire && wires.some(existing => existing.id === 'wire:' + number)) number++
  const wire = { id: rewire ?? 'wire:' + number, a, b }
  return rewire ? wires.map(existing => existing.id === rewire ? wire : existing) : [...wires, wire]
}

function hasPin(registry: Registry, ref: Terminal) {
  return devices.includes(ref.instanceId) && registry[ref.instanceId]?.some(pin => pin.id === ref.visualPinId)
}

function readObject(value: unknown, keys: string[]): Record<string, unknown> {
  if (!value || typeof value !== 'object' || Array.isArray(value) || Object.keys(value).sort().join('|') !== keys.sort().join('|')) {
    throw Error('Unexpected workspace fields')
  }
  return value as Record<string, unknown>
}

const schemaVersion = '1.0'
const qualification = 'VISUAL_ONLY_NOT_ENGINEERING_VERIFIED'
export function exportWorkspace(positions: PositionMap, wires: Wire[]) {
  return JSON.stringify({
    schemaVersion, qualification,
    nodes: devices.map(instanceId => ({
      instanceId, assetVariant: assets[instanceId].variant, assetRevision: assets[instanceId].revision,
      x: positions[instanceId].x, y: positions[instanceId].y,
    })),
    wires: [...wires].sort((a, b) => a.id < b.id ? -1 : a.id > b.id ? 1 : 0).map(({ id, a, b }) => ({ id, a, b })),
  }, null, 2)
}

export function importWorkspace(source: string, registry: Registry) {
  if (source.length > 250_000) throw Error('Workspace is too large')
  const root = readObject(JSON.parse(source), ['schemaVersion', 'qualification', 'nodes', 'wires'])
  if (root.schemaVersion !== schemaVersion || root.qualification !== qualification ||
      !Array.isArray(root.nodes) || root.nodes.length !== devices.length || !Array.isArray(root.wires)) throw Error('Unsupported workspace')
  const positions = {} as PositionMap
  const seen = new Set<Device>()
  for (const entry of root.nodes) {
    const { instanceId, assetVariant, assetRevision, x, y } = readObject(entry, ['instanceId', 'assetVariant', 'assetRevision', 'x', 'y'])
    const device = instanceId as Device
    if (!devices.includes(device) || seen.has(device) ||
        assetVariant !== assets[device].variant || assetRevision !== assets[device].revision ||
        typeof x !== 'number' || typeof y !== 'number' || !Number.isFinite(x) || !Number.isFinite(y) ||
        Math.abs(x) > 10000 || Math.abs(y) > 10000) throw Error('Unavailable device, stale asset revision or invalid position')
    seen.add(device)
    positions[device] = { x, y }
  }
  const readTerminal = (value: unknown): Terminal => {
    const { instanceId, visualPinId } = readObject(value, ['instanceId', 'visualPinId'])
    if (typeof instanceId !== 'string' || typeof visualPinId !== 'string') throw Error('Malformed terminal')
    const terminal = { instanceId: instanceId as Device, visualPinId }
    if (!hasPin(registry, terminal)) throw Error('Unavailable terminal')
    return terminal
  }
  const wires: Wire[] = []
  const wireIds = new Set<string>()
  const pairs = new Set<string>()
  for (const entry of root.wires) {
    const { id, a, b } = readObject(entry, ['id', 'a', 'b'])
    if (typeof id !== 'string' || !/^wire:[1-9][0-9]{0,5}$/.test(id) || wireIds.has(id)) throw Error('Invalid wire identity')
    const start = readTerminal(a)
    const end = readTerminal(b)
    const pair = pairKey(start, end)
    if (pairs.has(pair) || terminalKey(start) === terminalKey(end)) throw Error('Invalid wire pair')
    pairs.add(pair)
    wireIds.add(id)
    wires.push({ id, a: start, b: end })
  }
  return { positions, wires }
}
