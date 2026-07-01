import React from "react";
import "../styles/loop_visualizer.css";

interface LoopVisualizerProps {
  loopsCount: number;
  repeatingCommands: string[];
  isLoopBreakerActive: boolean;
}

export const LoopVisualizer: React.FC<LoopVisualizerProps> = ({
  loopsCount,
  repeatingCommands,
  isLoopBreakerActive,
}) => {
  return (
    <div className="loop-visualizer-card">
      <div className="loop-header">
        <h3>Trajectory Loop Detection</h3>
        <span className={`loop-status-badge ${isLoopBreakerActive ? "active" : "inactive"}`}>
          {isLoopBreakerActive ? "Breaker: ACTIVE" : "Breaker: MONITORING"}
        </span>
      </div>
      <div className="loop-body">
        <div className="loop-count-section">
          <span className="loop-count-val">{loopsCount}</span>
          <span className="loop-count-lbl">Infinite Loops Found</span>
        </div>
        {repeatingCommands.length > 0 && (
          <div className="loop-commands-list">
            <h4>Repeating Commands Log:</h4>
            <ul>
              {repeatingCommands.map((cmd, idx) => (
                <li key={idx} className="loop-cmd-item">
                  <code>{cmd}</code>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
};

export default LoopVisualizer;
