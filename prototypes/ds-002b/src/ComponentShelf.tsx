import { useRef, useState } from 'react'
import { assets, devices } from './model'
import type { Device } from './model'

type Props = {
  placed: ReadonlySet<Device>
  onPlace: (device: Device) => void
}

export function ComponentShelf({ placed, onPlace }: Props) {
  const dialog = useRef<HTMLDialogElement>(null)
  const opener = useRef<HTMLButtonElement>(null)
  const search = useRef<HTMLInputElement>(null)
  const [query, setQuery] = useState('')
  const term = query.trim().toLowerCase()
  const matches = devices.filter(device => device.includes(term) || assets[device].name.toLowerCase().includes(term))

  const open = () => {
    setQuery('')
    dialog.current?.showModal()
    search.current?.focus()
  }

  return <>
    <button lang="ka" ref={opener} type="button" onClick={open}>კომპონენტის დამატება</button>
    <dialog lang="ka" ref={dialog} aria-labelledby="shelf-title" onClose={() => opener.current?.focus()}>
      <h2 id="shelf-title">კომპონენტების ბიბლიოთეკა</h2>
      <label htmlFor="shelf-search">ძებნა</label>{' '}
      <input ref={search} id="shelf-search" type="search" value={query}
        onChange={event => setQuery(event.target.value)}
        onKeyDown={event => {
          if (event.key !== 'Escape') return
          // A filled native search field otherwise consumes Escape to clear its text.
          event.preventDefault()
          event.stopPropagation()
          dialog.current?.close()
        }} />
      {matches.length === 0 ? <p role="status">შედეგი ვერ მოიძებნა</p> : <ul>
        {matches.map(device => <li key={device}>
          {device === 'board' ? <span aria-disabled="true">ESP32-DevKitC-32E — ვიზუალი დაუმტკიცებელია</span> : <>
            <span>{assets[device].name}</span>{' '}
            {placed.has(device) ? <span>უკვე დამატებულია</span> :
              <button type="button" aria-label={assets[device].name + ' — მოთავსება'} onClick={() => {
                onPlace(device)
                dialog.current?.close()
              }}>მოთავსება</button>}
          </>}
        </li>)}
      </ul>}
    </dialog>
  </>
}
