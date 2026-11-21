import { useLayoutEffect, useRef, useState } from 'react'
import type { Ref } from 'react'
import { assets, devices } from './model'
import type { Device } from './model'

type Props = {
  placed: ReadonlySet<Device>
  onPlace: (device: Device) => void
  open: boolean
  opener: Ref<HTMLButtonElement>
  onOpen: () => void
  onClose: () => void
}

export function ComponentShelf({ placed, onPlace, open, opener, onOpen, onClose }: Props) {
  const search = useRef<HTMLInputElement>(null)
  const [query, setQuery] = useState('')
  const term = query.trim().toLowerCase()
  const matches = devices.filter(device => device.includes(term) || assets[device].name.toLowerCase().includes(term))

  useLayoutEffect(() => {
    if (open) search.current?.focus()
  }, [open])

  return <>
    <button lang="ka" ref={opener} type="button" aria-expanded={open} aria-controls="component-shelf" onClick={() => {
      if (open) onClose()
      else {
        setQuery('')
        onOpen()
      }
    }}>კომპონენტის დამატება</button>
    <section lang="ka" id="component-shelf" role="region" aria-labelledby="shelf-title"
      className="entry-panel shelf" data-open={open} inert={!open}>
      <div className="panel-heading">
        <h2 id="shelf-title">კომპონენტების ბიბლიოთეკა</h2>
        <button type="button" onClick={onClose}>დახურვა</button>
      </div>
      <label htmlFor="shelf-search">ძებნა</label>{' '}
      <input ref={search} id="shelf-search" type="search" value={query}
        onChange={event => setQuery(event.target.value)} />
      {matches.length === 0 ? <p role="status">შედეგი ვერ მოიძებნა</p> : <ul>
        {matches.map(device => <li key={device}>
          {device === 'board' ? <span aria-disabled="true">ESP32-DevKitC-32E — ვიზუალი დაუმტკიცებელია</span> : <>
            <span>{assets[device].name}</span>{' '}
            {placed.has(device) ? <span>უკვე დამატებულია</span> :
              <button type="button" aria-label={assets[device].name + ' — მოთავსება'} onClick={() => {
                onPlace(device)
                onClose()
              }}>მოთავსება</button>}
          </>}
        </li>)}
      </ul>}
    </section>
  </>
}
