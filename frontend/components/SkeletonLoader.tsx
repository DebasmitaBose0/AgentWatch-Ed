import React from "react";
import "../styles/dashboard_components.css";

interface SkeletonLoaderProps {
  width?: string;
  height?: string;
  borderRadius?: string;
}

export const SkeletonLoader: React.FC<SkeletonLoaderProps> = ({
  width = "100%",
  height = "20px",
  borderRadius = "4px",
}) => {
  return (
    <div
      className="skeleton-loader-container shimmer-animation"
      style={{ width, height, borderRadius }}
      data-testid="skeleton-loader"
    />
  );
};

export default SkeletonLoader;
