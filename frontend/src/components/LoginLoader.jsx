import React from "react";

export default function LoginLoader() {
  return (
    <div className="login-loader" role="status" aria-live="polite">
      <span className="login-loader-ring" aria-hidden="true" />
      <span className="login-loader-copy">
        <strong>Signing you in</strong>
        <small>Verifying secure access…</small>
      </span>
    </div>
  );
}
