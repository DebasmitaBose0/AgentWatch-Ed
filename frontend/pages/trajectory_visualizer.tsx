import React, { useState } from "react";
import LoopVisualizer from "../components/LoopVisualizer";

export const TrajectoryVisualizer: React.FC = () => {
  const [loops, setLoops] = useState(2);
  const [commands, setCommands] = useState([
    "cat config.json",
    "cat config.json",
    "cat config.json",
  ]);
  const [breakerActive, setBreakerActive] = useState(true);

  return (
    <div style={{ padding: "40px", background: "#0a0a0a", minHeight: "100vh" }}>
      <h1 style={{ color: "#fff", marginBottom: "24px" }}>AgentWatch Trajectory Loops</h1>
      <div style={{ maxWidth: "600px" }}>
        <LoopVisualizer
          loopsCount={loops}
          repeatingCommands={commands}
          isLoopBreakerActive={breakerActive}
        />
      </div>
    </div>
  );
};

export default TrajectoryVisualizer;
