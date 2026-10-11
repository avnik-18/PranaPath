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
  const [entered, setEntered] = useState(false)
  const [view, setView] = useState<View>(() =>
    window.location.hash === '#app' ? 'app' : 'landing',
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
  return <RoutingApp onOpenOps={() => setView('ops')} />
}
