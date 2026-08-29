import React from "react";

/**
 * Decorative login artwork. Change the scoped --scene-* variables in
 * styles.css to quickly retheme the evening scene.
 */
export default function EveningLoginScene() {
  return (
    <div className="login-scene" aria-hidden="true">
      <div className="scene-stars">
        {Array.from({ length: 18 }, (_, index) => (
          <i key={index} />
        ))}
      </div>
      <div className="scene-moon"><span /></div>
      <div className="scene-cloud scene-cloud-one" />
      <div className="scene-cloud scene-cloud-two" />
      <div className="scene-horizon" />
      <div className="scene-hill scene-hill-back" />
      <div className="scene-hill scene-hill-front" />
      <div className="scene-windmill">
        <div className="windmill-cap" />
        <div className="windmill-tower"><i /></div>
        <div className="windmill-blades">
          {Array.from({ length: 4 }, (_, index) => (
            <span key={index} style={{ "--blade-index": index }} />
          ))}
          <b />
        </div>
      </div>
      <div className="scene-grass" />
    </div>
  );
}
