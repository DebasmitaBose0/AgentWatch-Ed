import React from "react";
import "../styles/dashboard_components.css";

interface MetricCardProps {
  title: string;
  value: string | number;
  change?: string;
  isLoading?: boolean;
}

export const MetricCard: React.FC<MetricCardProps> = ({
  title,
  value,
  change,
  isLoading = false,
}) => {
  return (
    <div className="metric-card-container">
      <div className="metric-card-title">{title}</div>
      {isLoading ? (
        <div className="shimmer-animation skeleton-value" />
      ) : (
        <div className="metric-card-value">{value}</div>
      )}
      {change && !isLoading && (
        <div className={`metric-card-change ${change.startsWith("+") ? "positive" : "negative"}`}>
          {change}
        </div>
      )}
    </div>
  );
};

export default MetricCard;
