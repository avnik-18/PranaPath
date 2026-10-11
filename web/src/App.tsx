import { useState } from 'react'
import Home from './pages/Home'
import { Login } from './pages/Login'
import { Receipts } from './pages/Receipts'

export default function App() {
  // #app(-direct) = skip the demo sign-in (film capture / impatient users)
  const [entered, setEntered] = useState(() =>
    /#app(|-direct)/.test(window.location.hash))
  const [view, setView] = useState<'home' | 'receipts'>('home')

  if (!entered) return <Login onEnter={() => setEntered(true)} />
  if (view === 'receipts') return <Receipts onBack={() => setView('home')} />
  return <Home onOpenReceipts={() => setView('receipts')} />
}
