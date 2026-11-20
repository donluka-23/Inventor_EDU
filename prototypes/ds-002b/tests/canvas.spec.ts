import { expect, test } from '@playwright/test'
import type { Page } from '@playwright/test'
import { mkdir } from 'node:fs/promises'

const contact = (page: Page, key: string) => page.getByRole('button', { name: key, exact: true })
const wireCount = (page: Page) => page.locator('.wire-list li')
const status = (page: Page) => page.locator('.statusbar [role=status]')
const pathFor = (page: Page, wire: string) => page.locator('.react-flow__edge[data-id="' + wire + '"] path.react-flow__edge-path')
const pinCenter = async (page: Page, key: string) => contact(page, key).evaluate(element => {
  const rect = element.getBoundingClientRect()
  return { x: rect.x + rect.width / 2, y: rect.y + rect.height / 2 }
})
async function alignment(page: Page, wire: string, start: string, end: string) {
  const [a, b, path] = await Promise.all([
    pinCenter(page, start), pinCenter(page, end), pathFor(page, wire).evaluate(element => {
      const svg = element as SVGPathElement
      const matrix = svg.getScreenCTM()!
      return [svg.getPointAtLength(0), svg.getPointAtLength(svg.getTotalLength())].map(point => {
        const screen = point.matrixTransform(matrix)
        return { x: screen.x, y: screen.y }
      })
    }),
  ])
  return Math.max(Math.hypot(a.x - path[0].x, a.y - path[0].y), Math.hypot(b.x - path[1].x, b.y - path[1].y))
}

async function boardArtworkOffset(page: Page, key: string) {
  const pin = await pinCenter(page, key)
  return page.locator('.board-image').evaluate((image: HTMLImageElement, target) => {
    const canvas = document.createElement('canvas')
    canvas.width = image.naturalWidth
    canvas.height = image.naturalHeight
    const ctx = canvas.getContext('2d')!
    ctx.drawImage(image, 0, 0)
    const rect = image.getBoundingClientRect()
    const x = (target.x - rect.x) * canvas.width / rect.width
    const y = (target.y - rect.y) * canvas.height / rect.height
    const left = Math.floor(x) - 10
    const top = Math.floor(y) - 10
    const pixels = ctx.getImageData(left, top, 21, 21).data
    let count = 0
    let sumX = 0
    let sumY = 0
    for (let i = 0; i < pixels.length; i += 4) {
      if (pixels[i] > 190 && pixels[i + 1] > 145 && pixels[i + 2] < 110 && pixels[i + 3] === 255) {
        count++
        sumX += left + (i / 4) % 21 + .5
        sumY += top + Math.floor(i / 4 / 21) + .5
      }
    }
    if (!count) throw Error('No gold CAD contact within pin neighborhood')
    return Math.hypot((x - sumX / count) * rect.width / canvas.width, (y - sumY / count) * rect.height / canvas.height)
  }, pin)
}

async function sensorArtworkOffset(page: Page, key: string, index: number) {
  const center = await pinCenter(page, key)
  return page.locator('wokwi-hc-sr04').evaluate((element, { center, index }) => {
    const leads = Array.from(element.shadowRoot!.querySelectorAll<SVGRectElement>('rect'))
      .filter(rect => rect.getAttribute('y') === '19' && rect.getAttribute('height') === '7')
    const lead = leads[index]
    const box = lead.getBBox()
    const matrix = lead.getScreenCTM()!
    const top = new DOMPoint(box.x + box.width / 2, box.y).matrixTransform(matrix)
    const end = new DOMPoint(box.x + box.width / 2, box.y + box.height).matrixTransform(matrix)
    return Math.hypot(center.x - top.x, Math.max(top.y - center.y, center.y - end.y, 0))
  }, { center, index })
}

async function dragPart(page: Page, device: string, dx: number, dy: number) {
  const label = page.locator('[data-device="' + device + '"] .part-label')
  const bounds = (await label.boundingBox())!
  const x = bounds.x + bounds.width / 2
  const y = bounds.y + bounds.height / 2
  await page.mouse.move(x, y)
  await page.mouse.down()
  await page.mouse.move(x + dx, y + dy, { steps: 9 })
  await page.mouse.up()
}

test('real pointer wiring, independent ECHO, all contacts, geometry and portable visual JSON', async ({ page, browser }) => {
  console.log('Chromium ' + browser.version())
  const external: string[] = []
  const scriptErrors: string[] = []
  page.on('request', request => {
    if (!request.url().startsWith('http://127.0.0.1:4173') && !request.url().startsWith('data:')) external.push(request.url())
  })
  page.on('pageerror', error => scriptErrors.push(error.message))
  await page.goto('/')
  await expect(page.locator('[data-terminal]')).toHaveCount(46)
  const boardPins = await page.locator('[data-device=board] [data-terminal]').evaluateAll(handles => handles.map(handle => {
    const box = handle.getBoundingClientRect()
    return { id: handle.getAttribute('data-terminal'), x: box.left, y: box.top, tabIndex: (handle as HTMLElement).tabIndex }
  }))
  expect(new Set(boardPins.map(pin => pin.id)).size).toBe(38)
  expect(boardPins.every(pin => pin.tabIndex === 0)).toBe(true)
  for (let index = 0; index < 19; index++) {
    expect(boardPins[index].id).toBe('board/J2.' + (index + 1))
    expect(boardPins[index + 19].id).toBe('board/J3.' + (index + 1))
    expect(boardPins[index].x).toBeLessThan(boardPins[index + 19].x)
    if (index) expect(boardPins[index].y - boardPins[index - 1].y).toBeGreaterThan(11)
  }
  const maxBoard = Math.max(...await Promise.all(boardPins.map(pin => boardArtworkOffset(page, pin.id!))))
  expect(maxBoard).toBeLessThan(1)
  await contact(page, 'sensor/TRIG').hover()
  await expect(page.locator('.contact-readout')).toContainText('sensor/TRIG')
  await contact(page, 'sensor/TRIG').click()
  await expect(wireCount(page)).toHaveCount(0)
  await page.keyboard.press('Escape')
  await expect(status(page)).toContainText('Draft canceled')
  await contact(page, 'sensor/TRIG').click()
  await contact(page, 'sensor/TRIG').click()
  await expect(status(page)).toContainText('different contacts')
  await contact(page, 'board/J2.5').click()
  await expect(pathFor(page, 'wire:1')).toBeVisible()
  await expect.poll(() => alignment(page, 'wire:1', 'sensor/TRIG', 'board/J2.5')).toBeLessThan(2)
  const firstPath = await pathFor(page, 'wire:1').getAttribute('d')
  await contact(page, 'sensor/ECHO').click()
  await contact(page, 'board/J3.8').click()
  const echoPath = await pathFor(page, 'wire:2').getAttribute('d')
  await contact(page, 'board/J2.5').click()
  await contact(page, 'sensor/TRIG').click()
  await expect(status(page)).toContainText('already exists')
  await page.keyboard.press('Escape')
  await page.locator('.wire-list button').filter({ hasText: 'sensor/TRIG' }).click()
  await page.getByRole('button', { name: 'Rewire destination' }).click()
  await contact(page, 'board/J3.9').click()
  await expect(pathFor(page, 'wire:1')).not.toHaveAttribute('d', firstPath!)
  await expect(pathFor(page, 'wire:2')).toHaveAttribute('d', echoPath!)
  await expect(wireCount(page)).toHaveCount(2)
  await expect(page.locator('.contact-readout')).toContainText('CANONICAL_MAPPING_UNAVAILABLE')
  await mkdir('evidence', { recursive: true })
  await contact(page, 'board/J3.9').hover()
  await page.screenshot({ path: 'evidence/workspace-1440x900.png' })
  const start = await pinCenter(page, 'sensor/TRIG')
  const end = await pinCenter(page, 'board/J3.9')
  await dragPart(page, 'sensor', -37, 52)
  await dragPart(page, 'board', 49, 25)
  expect((await pinCenter(page, 'sensor/TRIG')).y - start.y).toBeGreaterThan(45)
  expect((await pinCenter(page, 'board/J3.9')).x - end.x).toBeGreaterThan(42)
  await page.mouse.move(60, 715)
  await page.mouse.down()
  await page.mouse.move(90, 743, { steps: 8 })
  await page.mouse.up()
  expect((await pinCenter(page, 'board/J3.9')).x - end.x).toBeGreaterThan(70)
  await page.getByRole('button', { name: 'Fit view' }).click()
  for (const zoom of [.5, 1, 2]) {
    await page.getByRole('button', { name: 'Zoom ' + zoom + 'x', exact: true }).click()
    await expect(page.getByLabel('Current zoom')).toHaveText((zoom * 100) + '%')
    await expect.poll(() => alignment(page, 'wire:1', 'sensor/TRIG', 'board/J3.9')).toBeLessThan(2)
    const edgeOffset = await alignment(page, 'wire:1', 'sensor/TRIG', 'board/J3.9')
    const boardOffset = await boardArtworkOffset(page, 'board/J3.9')
    const sensorOffset = await sensorArtworkOffset(page, 'sensor/TRIG', 1)
    expect(boardOffset).toBeLessThan(2)
    expect(sensorOffset).toBeLessThan(3)
    console.log({ zoom, edgeOffset, boardOffset, sensorOffset, allBoardAtStartMax: maxBoard })
    if (zoom === 2) {
      await contact(page, 'board/J3.9').hover()
      await page.screenshot({ path: 'evidence/contact-zoom-2x.png' })
    }
  }
  await page.setViewportSize({ width: 1024, height: 768 })
  await page.getByRole('button', { name: 'Fit view' }).click()
  await expect.poll(() => alignment(page, 'wire:1', 'sensor/TRIG', 'board/J3.9')).toBeLessThan(2)
  await contact(page, 'board/J3.9').hover()
  await page.screenshot({ path: 'evidence/workspace-1024x768.png' })

  await page.getByText('Visual workspace JSON', { exact: true }).click()
  await page.getByRole('button', { name: 'Export', exact: true }).click()
  const data = await page.getByLabel('Workspace data').inputValue()
  const exported = JSON.parse(data)
  expect(exported.qualification).toBe('VISUAL_ONLY_NOT_ENGINEERING_VERIFIED')
  expect(exported.wires.map((wire: { b: { visualPinId: string } }) => wire.b.visualPinId)).toEqual(['J3.9', 'J3.8'])
  expect(data).not.toMatch(/canonicalTerminal|catalogDigest|CircuitSnapshot|GpioFinding/)
  await page.reload()
  await expect(page.locator('[data-terminal]')).toHaveCount(46)
  await page.getByText('Visual workspace JSON', { exact: true }).click()
  const textarea = page.getByLabel('Workspace data')
  await textarea.fill(data.replace('innerscene-v4-nominal-wroom', 'fake-v1'))
  await page.getByRole('button', { name: 'Import', exact: true }).click()
  await expect(status(page)).toContainText('Import rejected')
  await expect(wireCount(page)).toHaveCount(0)
  await textarea.fill(data)
  await page.getByRole('button', { name: 'Import', exact: true }).click()
  await expect(wireCount(page)).toHaveCount(2)
  await page.getByRole('button', { name: 'Export', exact: true }).click()
  await expect(textarea).toHaveValue(data)
  expect(external).toEqual([])
  expect(scriptErrors).toEqual([])
})

test('keyboard navigation, passive leads, undo and redo, and invalidated Lit geometry', async ({ page }) => {
  await page.goto('/')
  await expect(page.locator('[data-terminal]')).toHaveCount(46)
  let discovered = false
  for (let i = 0; i < 68; i++) {
    if (await contact(page, 'board/J2.1').evaluate(element => document.activeElement === element)) { discovered = true; break }
    await page.keyboard.press('Tab')
  }
  expect(discovered).toBe(true)
  await page.keyboard.press('Enter')
  await page.keyboard.press('Tab')
  await expect(contact(page, 'board/J2.2')).toBeFocused()
  await page.keyboard.press('Space')
  await expect(wireCount(page)).toHaveCount(1)
  await page.keyboard.press('Delete')
  await expect(wireCount(page)).toHaveCount(0)
  await page.keyboard.press('Control+z')
  await expect(wireCount(page)).toHaveCount(1)
  await page.keyboard.press('Control+Shift+z')
  await expect(wireCount(page)).toHaveCount(0)
  const ledX = (await pinCenter(page, 'led/A')).x
  await page.locator('wokwi-led').evaluate(element => element.setAttribute('flip', ''))
  await expect.poll(async () => Math.abs((await pinCenter(page, 'led/A')).x - ledX)).toBeGreaterThan(15)
  await contact(page, 'led/A').click()
  await contact(page, 'resistor/1').click()
  await expect(wireCount(page)).toHaveCount(1)
  await expect.poll(() => alignment(page, 'wire:1', 'led/A', 'resistor/1')).toBeLessThan(2)
  await contact(page, 'led/C').focus()
  await expect(contact(page, 'led/C')).toBeFocused()
  await page.keyboard.press('Enter')
  await expect(page.locator('.draft')).toContainText('led/C')
  await contact(page, 'resistor/2').focus()
  await expect(contact(page, 'resistor/2')).toBeFocused()
  await page.keyboard.press('Enter')
  await expect(wireCount(page)).toHaveCount(2)
  await page.locator('wokwi-led').evaluate(element => {
    Object.defineProperty(element, 'pinInfo', { value: [{ name: 'A', x: 4, y: 5 }] })
    element.setAttribute('data-test-mutated', '')
  })
  await expect(contact(page, 'led/A')).toHaveCount(0)
  await expect(page.getByRole('alert')).toContainText('Incomplete pin geometry')
  await expect(pathFor(page, 'wire:1')).toHaveCount(0)
})

test('missing board image removes only board handles', async ({ page }) => {
  await page.route('**/devkitc-v4.png', route => route.fulfill({ status: 404, body: 'missing' }))
  await page.goto('/')
  await expect(page.locator('[data-device=board] [data-terminal]')).toHaveCount(0)
  await expect(page.locator('[data-terminal]')).toHaveCount(8)
  await expect(page.getByRole('alert')).toContainText('Board image unavailable')
  await contact(page, 'led/C').click()
  await contact(page, 'resistor/2').click()
  await expect(wireCount(page)).toHaveCount(1)
})

test('stale board image digest cannot expose pin handles', async ({ page }) => {
  await page.route('**/devkitc-v4.png', route => route.fulfill({ status: 200, contentType: 'image/png', body: 'bad bytes' }))
  await page.goto('/')
  await expect(page.getByRole('alert')).toContainText('Board asset digest mismatch')
  await expect(page.locator('[data-device=board] [data-terminal]')).toHaveCount(0)
  await expect(page.locator('[data-terminal]')).toHaveCount(8)
})

test('DPR 2 and dense contacts preserve named pointer and keyboard targets', async ({ browser }) => {
  const page = await browser.newPage({ viewport: { width: 1024, height: 768 }, deviceScaleFactor: 2 })
  try {
    await page.goto('http://127.0.0.1:4173/')
    await expect(page.locator('[data-terminal]')).toHaveCount(46)
    expect(await page.evaluate(() => devicePixelRatio)).toBe(2)
    await page.getByRole('button', { name: 'Zoom 0.5x', exact: true }).click()
    await contact(page, 'board/J2.5').click()
    await contact(page, 'board/J2.6').click()
    await expect(page.locator('.wire-list')).toContainText('board/J2.5 → board/J2.6')
    await expect.poll(() => alignment(page, 'wire:1', 'board/J2.5', 'board/J2.6')).toBeLessThan(2)
    await page.getByLabel('Find a physical contact').selectOption('board/J3.19')
    await page.getByRole('button', { name: 'Focus', exact: true }).focus()
    await page.keyboard.press('Enter')
    await expect(contact(page, 'board/J3.19')).toBeFocused()
    await expect(page.getByLabel('Current zoom')).toHaveText('100%')
    await expect(page.locator('.contact-readout')).toContainText('board/J3.19')
  } finally {
    await page.close()
  }
})
