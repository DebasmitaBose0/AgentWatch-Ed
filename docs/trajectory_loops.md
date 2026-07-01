# Trajectory Loop Visualizer (ELUSoC_2026)

## Background
AI agents occasionally enter endless recursive loop cycles calling the same tools repetitively (e.g. reading a configuration file repeatedly due to state bugs).

## Solution
We introduce a trajectory loop visualizer interface allowing developers to inspect repeating patterns in real-time. It maps out recursion counts and allows viewing loop breaker states.

## Files
- `frontend/components/LoopVisualizer.tsx` - pulsing alert card indicating loop parameters.
- `frontend/styles/loop_visualizer.css` - custom layout design styles.
- `frontend/pages/trajectory_visualizer.tsx` - preview dashboard demonstrating detection.
