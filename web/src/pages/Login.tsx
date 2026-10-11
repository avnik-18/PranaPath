type Props = { onEnter: () => void }

export function Login(p: Props) {
  return (
    <div className="login">
      <div className="login-card">
        <div className="brand">
          <span className="logo-dot" />
          <b>PranaPath</b>
        </div>
        <div className="login-kicker">breathe-safe routing · engine console</div>
        <label className="login-field">
          <span>email</span>
          <input value="guest@pranapath.app" readOnly />
        </label>
        <label className="login-field">
          <span>password</span>
          <input value="guest-pass" readOnly type="password" />
        </label>
        <button className="login-cta" onClick={p.onEnter}>Sign in as guest</button>
        <div className="login-note">
          guest pass — one click · the ops console unlocks behind the same session
        </div>
      </div>
    </div>
  )
}
