import { expect, test } from '@playwright/test'
import type { Page } from '@playwright/test'
import { mkdir } from 'node:fs/promises'

const add = (page: Page) => page.getByRole('button', { name: 'კომპონენტის დამატება' })
const shelf = (page: Page) => page.getByRole('dialog', { name: 'კომპონენტების ბიბლიოთეკა' })
const search = (page: Page) => shelf(page).getByRole('searchbox', { name: 'ძებნა' })
const place = (page: Page, name: string) => shelf(page).getByRole('button', { name: name + ' — მოთავსება' })
const pin = (page: Page, id: string) => page.getByRole('button', { name: id, exact: true })
const part = (page: Page, id: string) => page.locator('.react-flow__node[data-id="' + id + '"]')
const wire = (page: Page) => page.locator('.react-flow__edge-path')

async function addPart(page: Page, name: string) {
  await add(page).click()
  await place(page, name).click()
  await expect(shelf(page)).toBeHidden()
  await expect(add(page)).toBeFocused()
}

async function position(page: Page, id: string) {
  return part(page, id).evaluate(element => {
    const matrix = new DOMMatrix(getComputedStyle(element).transform)
    return { x: matrix.m41, y: matrix.m42 }
  })
}

async function edgeOffset(page: Page) {
  const endpoints = await wire(page).evaluate(element => {
    const path = element as SVGPathElement
    const matrix = path.getScreenCTM()!
    return [0, path.getTotalLength()].map(distance => {
      const { x, y } = path.getPointAtLength(distance).matrixTransform(matrix)
      return { x, y }
    })
  })
  const handles = await Promise.all(['sensor/TRIG', 'led/A'].map(id => pin(page, id).evaluate(element => {
    const { x, y, width, height } = element.getBoundingClientRect()
    return { x: x + width / 2, y: y + height / 2 }
  })))
  return Math.max(...handles.map((handle, index) =>
    Math.hypot(handle.x - endpoints[index].x, handle.y - endpoints[index].y)))
}

test('UXN-01 legacy root and non-exact URLs retain the four-part canvas', async ({ page }) => {
  await page.goto('/')
  await expect(page.locator('.react-flow__node')).toHaveCount(4)
  await expect(page.locator('[data-terminal]')).toHaveCount(46)
  await expect(page.getByText('Visual workspace JSON', { exact: true })).toBeVisible()
  await expect(add(page)).toHaveCount(0)
  await page.goto('/?ux=entry&extra=1')
  await expect(page.locator('.react-flow__node')).toHaveCount(4)
  await expect(add(page)).toHaveCount(0)
})

test('UXN-02, 06, 07 exact entry starts empty and keeps unsupported features absent', async ({ page }) => {
  await page.goto('/?ux=entry')
  await expect(page.getByRole('heading', { name: 'INVENTOR EDU — ვიზუალური ექსპერიმენტი' })).toBeVisible()
  await expect(page.getByText('VISUAL_ONLY_NOT_ENGINEERING_VERIFIED', { exact: true })).toBeVisible()
  await expect(page.getByRole('region', { name: 'Circuit canvas' }).locator('.react-flow')).toBeVisible()
  await expect(add(page)).toHaveCount(1)
  await expect(page.locator('.react-flow__node, .board-image, [data-terminal]')).toHaveCount(0)
  await expect(page.getByText('კომპონენტები ჯერ არ არის დამატებული')).toBeVisible()
  await expect(page.getByText('კონტაქტი არ არის არჩეული')).toBeVisible()
  await expect(page.getByText(/^(Visual workspace JSON|Save|Saved|Recent|Recover|Assistant|Lesson|PASS)$/i)).toHaveCount(0)
  await add(page).click()
  const board = shelf(page).getByText('ESP32-DevKitC-32E — ვიზუალი დაუმტკიცებელია', { exact: true })
  await expect(board).toHaveAttribute('aria-disabled', 'true')
  await expect(board.locator('..').getByRole('button')).toHaveCount(0)
  await search(page).fill('board')
  await expect(shelf(page).getByRole('listitem')).toHaveCount(1)
  await page.keyboard.press('Escape')
  await expect(shelf(page)).toBeHidden()
  await expect(add(page)).toBeFocused()
  await expect(page.locator('.react-flow__node')).toHaveCount(0)
})

test('UXN-03 shelf filters by fixed ID and name and Escape preserves a draft and viewport', async ({ page }) => {
  await page.goto('/?ux=entry')
  await add(page).click()
  await expect(search(page)).toBeFocused()
  await expect(shelf(page).getByRole('listitem')).toHaveCount(4)
  for (const term of ['SeNsOr', 'hc-Sr04']) {
    await search(page).fill(term)
    await expect(shelf(page).getByRole('listitem')).toHaveCount(1)
    await expect(place(page, 'HC-SR04')).toBeVisible()
  }
  await search(page).fill('arbitrary-typed-device')
  await expect(shelf(page).getByRole('status')).toHaveText('შედეგი ვერ მოიძებნა')
  await expect(shelf(page).getByRole('button')).toHaveCount(0)
  await page.keyboard.press('Enter')
  await expect(shelf(page)).toBeVisible()
  await page.keyboard.press('Escape')
  await expect(add(page)).toBeFocused()
  await expect(page.locator('.react-flow__node')).toHaveCount(0)
  await addPart(page, 'HC-SR04')
  await pin(page, 'sensor/TRIG').click()
  await expect(page.locator('.draft')).toContainText('sensor/TRIG')
  await page.getByRole('button', { name: 'Zoom 0.5x', exact: true }).click()
  const before = await position(page, 'sensor')
  await add(page).click()
  await page.keyboard.press('Escape')
  await expect(shelf(page)).toBeHidden()
  await expect(add(page)).toBeFocused()
  await expect(page.locator('.draft')).toContainText('sensor/TRIG')
  await expect(page.locator('.contact-readout')).toContainText('sensor/TRIG')
  await expect(page.getByLabel('Current zoom')).toHaveText('50%')
  expect(await position(page, 'sensor')).toEqual(before)
  await expect(wire(page)).toHaveCount(0)
})

test('UXN-04, 05 placements and wire edits keep existing nodes and renderer geometry', async ({ page }) => {
  await page.goto('/?ux=entry')
  await addPart(page, 'HC-SR04')
  await expect(page.locator('wokwi-hc-sr04 svg')).toBeVisible()
  await expect(part(page, 'sensor').locator('[data-terminal]')).toHaveCount(4)
  expect(await position(page, 'sensor')).toEqual({ x: 430, y: 157 })
  await pin(page, 'sensor/TRIG').click()
  await page.getByRole('button', { name: 'Zoom 0.5x', exact: true }).click()
  await addPart(page, 'LED')
  await expect(page.getByLabel('Current zoom')).toHaveText('50%')
  await expect(page.locator('.contact-readout')).toContainText('sensor/TRIG')
  expect(await position(page, 'sensor')).toEqual({ x: 430, y: 157 })
  expect(await position(page, 'led')).toEqual({ x: 455, y: 369 })
  await expect(page.locator('wokwi-led svg')).toBeVisible()
  await expect(part(page, 'led').locator('[data-terminal]')).toHaveCount(2)
  await pin(page, 'led/A').click()
  await expect(page.locator('.wire-list')).toContainText('sensor/TRIG → led/A')
  await expect(wire(page)).toHaveCount(1)
  await expect(page.locator('.contact-readout')).toContainText('CANONICAL_MAPPING_UNAVAILABLE')
  await add(page).click()
  await expect(shelf(page).getByText('უკვე დამატებულია', { exact: true })).toHaveCount(2)
  await expect(place(page, 'HC-SR04')).toHaveCount(0)
  await expect(place(page, 'LED')).toHaveCount(0)
  await place(page, 'Resistor').click()
  await expect(page.locator('wokwi-resistor svg')).toBeVisible()
  await expect(page.locator('.react-flow__node')).toHaveCount(3)
  await expect(wire(page)).toHaveCount(1)
  await expect(page.locator('.wire-list button')).toHaveAttribute('aria-pressed', 'true')
  await expect(page.getByLabel('Current zoom')).toHaveText('50%')

  await page.getByRole('button', { name: 'Zoom 1x', exact: true }).click()
  const before = await wire(page).getAttribute('d')
  const oldPosition = await position(page, 'led')
  const label = await part(page, 'led').locator('.part-label').boundingBox()
  if (!label) throw Error('LED label was outside the canvas')
  await page.mouse.move(label.x + label.width / 2, label.y + label.height / 2)
  await page.mouse.down()
  await page.mouse.move(label.x + label.width / 2 + 55, label.y + label.height / 2 + 15, { steps: 8 })
  await page.mouse.up()
  await expect.poll(() => position(page, 'led')).not.toEqual(oldPosition)
  await expect(wire(page)).not.toHaveAttribute('d', before!)

  const viewport = page.getByRole('region', { name: 'Circuit canvas' }).locator('.react-flow__viewport')
  const transform = await viewport.evaluate(element => getComputedStyle(element).transform)
  await page.mouse.move(120, 170)
  await page.mouse.down()
  await page.mouse.move(175, 205, { steps: 8 })
  await page.mouse.up()
  await expect.poll(() => viewport.evaluate(element => getComputedStyle(element).transform)).not.toBe(transform)

  for (const zoom of [0.5, 1, 2]) {
    await page.getByRole('button', { name: 'Zoom ' + zoom + 'x', exact: true }).click()
    await expect(page.getByLabel('Current zoom')).toHaveText(zoom * 100 + '%')
    await expect.poll(() => edgeOffset(page)).toBeLessThan(2)
    console.log('Entry sensor/TRIG–led/A at ' + zoom + '×: ' + (await edgeOffset(page)).toFixed(4) + ' CSS px')
  }
  await page.getByRole('button', { name: /Undo/ }).click()
  await expect(wire(page)).toHaveCount(0)
  await page.getByRole('button', { name: /Redo/ }).click()
  await expect(wire(page)).toHaveCount(1)
  await expect.poll(() => edgeOffset(page)).toBeLessThan(2)
})

test('UXN-04 renderer failure withholds contacts and the shelf keeps working', async ({ page }) => {
  await page.goto('/?ux=entry')
  await addPart(page, 'LED')
  await expect(pin(page, 'led/A')).toBeVisible()
  await page.locator('wokwi-led').evaluate(element => {
    Object.defineProperty(element, 'pinInfo', { value: [] })
    element.setAttribute('data-invalid-pin-info', 'true')
  })
  await expect(part(page, 'led').locator('[data-terminal]')).toHaveCount(0)
  await expect(page.getByRole('alert')).toContainText('Incomplete pin geometry')
  await addPart(page, 'Resistor')
  await expect(part(page, 'resistor').locator('[data-terminal]')).toHaveCount(2)
  await expect(part(page, 'led').locator('[data-terminal]')).toHaveCount(0)
})

for (const size of [{ width: 1440, height: 900 }, { width: 1024, height: 768 }]) {
  test('UXN-08 keyboard journey and capture at ' + size.width + '×' + size.height, async ({ page, baseURL, browser }) => {
    const errors: string[] = []
    const external: string[] = []
    const boardImages: string[] = []
    page.on('pageerror', error => errors.push(error.message))
    page.on('request', request => {
      const url = new URL(request.url())
      if (!['data:', 'blob:'].includes(url.protocol) && url.origin !== new URL(baseURL!).origin) external.push(url.href)
      if (request.resourceType() === 'image' && url.pathname.includes('devkitc-v4')) boardImages.push(url.href)
    })
    await page.setViewportSize(size)
    await page.goto('/?ux=entry')
    await page.keyboard.press('Tab')
    await expect(add(page)).toBeFocused()
    for (const [term, name] of [['sensor', 'HC-SR04'], ['LED', 'LED']]) {
      await page.keyboard.press('Enter')
      await expect(search(page)).toBeFocused()
      await page.keyboard.type(term)
      await page.keyboard.press('Tab')
      await expect(place(page, name)).toBeFocused()
      await page.keyboard.press('Enter')
      await expect(shelf(page)).toBeHidden()
      await expect(add(page)).toBeFocused()
    }
    await expect(page.locator('[data-terminal]')).toHaveCount(6)
    for (const id of ['sensor/TRIG', 'led/A']) {
      for (let step = 0; step < 24; step++) {
        if (await pin(page, id).evaluate(element => element === document.activeElement)) break
        await page.keyboard.press('Tab')
      }
      await expect(pin(page, id)).toBeFocused()
      await page.keyboard.press('Enter')
    }
    await expect(wire(page)).toHaveCount(1)
    await expect(page.locator('.contact-readout')).toContainText('led/A')
    await expect(page.getByText('TEST_ONLY · SEMANTIC_EXPERIMENT_NOT_VISUAL_DESIGN', { exact: true })).toBeVisible()
    await expect(page.getByText('VISUAL_ONLY_NOT_ENGINEERING_VERIFIED', { exact: true })).toBeVisible()
    if (size.width === 1024) await add(page).click()
    await mkdir('evidence', { recursive: true })
    await page.screenshot({ path: 'evidence/ux-nav-001a-entry-' + size.width + 'x' + size.height + '.png' })
    if (size.width === 1024) {
      await expect(search(page)).toBeFocused()
      await page.keyboard.press('Escape')
      await expect(add(page)).toBeFocused()
    }
    expect(errors).toEqual([])
    expect(external).toEqual([])
    expect(boardImages).toEqual([])
    console.log('Entry screenshot ' + size.width + '×' + size.height + ', Chromium ' + browser.version())
  })
}
