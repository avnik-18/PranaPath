import { useState } from 'react'
import RoutingApp from './components/RoutingApp'
import { AwsOps } from './components/aws/AwsOps'
import { LoginGate } from './components/entry/LoginGate'
import { Navigation } from './components/landing/Navigation'
import { Hero } from './components/landing/Hero'
import { Marquee } from './components/landing/Marquee'
import { AboutTrap } from './components/landing/AboutTrap'
import { SystemRings } from './components/landing/SystemRings'
import { ProofStrip } from './components/landing/ProofStrip'
import { HonestLimits } from './components/landing/HonestLimits'
import { Footer } from './components/landing/Footer'

type View = 'landing' | 'app' | 'ops'

export default function App() {
  // #app-direct = skip the demo sign-in (film capture / impatient users)
  const [entered, setEntered] = useState(() =>
    /#app(|-direct)/.test(window.location.hash))
  // default face = the PRODUCT (map); landing is the optional story (#home)
  const [view, setView] = useState<View>(() =>
    window.location.hash === '#home' ? 'landing' : 'app',
  )

  if (!entered) return <LoginGate onEnter={() => setEntered(true)} />

  if (view === 'landing') {
    return (
      <div className="landing">
        <Navigation onOpenApp={() => {
          window.location.hash = '#app'
          setView('app')
        }} />
        <Hero onOpenApp={() => {
          window.location.hash = '#app'
          setView('app')
        }} />
        <Marquee />
        <main className="l-body">
          <AboutTrap />
          <SystemRings />
          <ProofStrip />
          <HonestLimits />
        </main>
        <Footer />
      </div>
    )
  }
  if (view === 'ops') {
    return <AwsOps onBack={() => setView('app')} />
  }
  return <RoutingApp
    onOpenOps={() => setView('ops')}
    onHome={() => setView('landing')} />
}
