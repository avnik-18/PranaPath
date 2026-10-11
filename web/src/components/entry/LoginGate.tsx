type Props = { onEnter: () => void }

export function LoginGate(p: Props) {
  return (
    <div className="login">
      <div className="login-card">
        <div className="brand">
          <span className="logo-dot" />
          <b>EcoRoute AI</b>
        </div>
        <div className="login-kicker">breathe-safe routing · demo console</div>
        <label className="login-field">
          <span>email</span>
          <input value="demo@ecoroute.ai" readOnly />
        </label>
        <label className="login-field">
          <span>password</span>
          <input value="demo-not-real" readOnly type="password" />
        </label>
        <button className="login-cta" onClick={p.onEnter}>Sign in as demo</button>
        <div className="login-note">
          demo sign-in — no real auth tonight, one click · ops console unlocks behind the same session
        </div>
      </div>
    </div>
  )
}
