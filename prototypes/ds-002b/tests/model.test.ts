import test from 'node:test'
import assert from 'node:assert/strict'
import { changeWire, exportWorkspace, importWorkspace, initialPositions, validatePins } from '../src/model.ts'
import type { Registry, Terminal } from '../src/model.ts'

const a: Terminal = { instanceId: 'sensor', visualPinId: 'TRIG' }
const b: Terminal = { instanceId: 'board', visualPinId: 'J2.5' }
const c: Terminal = { instanceId: 'board', visualPinId: 'J3.9' }
const registry: Registry = {
  sensor: [{ id: 'TRIG', x: 30, y: 40 }],
  board: [{ id: 'J2.5', x: 10, y: 16 }, { id: 'J3.9', x: 55, y: 14 }],
  led: [{ id: 'A', x: 4, y: 6 }],
  resistor: [{ id: '1', x: 1, y: 1 }],
}
test('validated contact geometry rejects missing, overlapping, duplicate and poisoned rows', () => {
  const pins = [{ id: '1', x: 0, y: 2 }, { id: '2', x: 12, y: 2 }]
  assert.deepEqual(validatePins('resistor', [...pins].reverse(), 12, 4), pins)
  assert.throws(() => validatePins('resistor', [pins[0]], 12, 4))
  assert.throws(() => validatePins('resistor', [pins[0], { ...pins[1], x: 10 }], 12, 4))
  assert.throws(() => validatePins('resistor', [pins[0], { ...pins[1], id: '1' }], 12, 4))
  assert.throws(() => validatePins('resistor', [pins[0], { ...pins[1], y: NaN }], 12, 4))
  assert.throws(() => validatePins('resistor', [pins[0], { ...pins[1], id: '<script>' }], 12, 4))
})
test('rewiring changes only the destination and preserves wire identity', () => {
  const wires = changeWire([], a, b, registry)
  const second = changeWire(wires, b, c, registry)
  const result = changeWire(second, a, c, registry, wires[0].id)
  assert.deepEqual(result[0], { id: 'wire:1', a, b: c })
  assert.equal(result[1], second[1])
  assert.deepEqual(wires[0].b, b)
  assert.throws(() => changeWire(result, c, a, registry), /already exists/)
  assert.throws(() => changeWire(result, c, c, registry), /different contacts/)
  assert.throws(() => changeWire(result, a, { ...c, visualPinId: 'bad' }, registry), /unavailable/)
})
test('deterministic exchange fails closed for stale source, variants and fabricated terminal data', () => {
  const wires = changeWire([], a, b, registry)
  const data = exportWorkspace(initialPositions, wires)
  const loaded = importWorkspace(data, registry)
  assert.equal(exportWorkspace(loaded.positions, loaded.wires), data)
  for (const mutate of [
    (value: any) => { value.nodes[0].assetRevision = 'sha256:stale' },
    (value: any) => { value.nodes[0].assetVariant = 'devkitc-v1' },
    (value: any) => { value.wires[0].b.visualPinId = 'J3.20' },
    (value: any) => { value.wires[0].b.canonicalTerminal = { terminalId: 'J2.5' } },
    (value: any) => { value.wires[0].id = 'wire:1<script>' },
    (value: any) => { value.schemaVersion = '2.0' },
  ]) {
    const edited = JSON.parse(data)
    mutate(edited)
    assert.throws(() => importWorkspace(JSON.stringify(edited), registry))
  }
  assert.throws(() => importWorkspace(data, { ...registry, board: [] }))
  assert.throws(() => importWorkspace('{bad json', registry))
})
