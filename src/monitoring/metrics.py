"""
Metrics collection and monitoring
Tracks latency, prediction counts, and performance metrics
"""

import time
from typing import Dict, List
from datetime import datetime
from collections import defaultdict
from threading import Lock


class MetricsCollector:
    """
    Thread-safe metrics collector for production monitoring
    Tracks prediction latencies, counts, and confidence scores
    """
    
    def __init__(self):
        self._lock = Lock()
        self._latencies: Dict[str, List[float]] = defaultdict(list)
        self._prediction_counts: Dict[str, Dict[str, int]] = defaultdict(
            lambda: {"success": 0, "failure": 0}
        )
        self._confidence_scores: Dict[str, List[float]] = defaultdict(list)
        self._low_confidence_events: List[Dict] = []
        
    def record_latency(self, model_name: str, latency_ms: float):
        """Record prediction latency"""
        with self._lock:
            self._latencies[model_name].append(latency_ms)
            # Keep only last 1000 measurements
            if len(self._latencies[model_name]) > 1000:
                self._latencies[model_name] = self._latencies[model_name][-1000:]
    
    def record_prediction(self, model_name: str, success: bool):
        """Record prediction success/failure"""
        with self._lock:
            if success:
                self._prediction_counts[model_name]["success"] += 1
            else:
                self._prediction_counts[model_name]["failure"] += 1
    
    def record_confidence(self, model_name: str, confidence: float, threshold: float):
        """Record confidence score and flag low confidence predictions"""
        with self._lock:
            self._confidence_scores[model_name].append(confidence)
            
            # Keep only last 1000 scores
            if len(self._confidence_scores[model_name]) > 1000:
                self._confidence_scores[model_name] = self._confidence_scores[model_name][-1000:]
            
            # Log low confidence events
            if confidence < threshold:
                self._low_confidence_events.append({
                    "model": model_name,
                    "confidence": confidence,
                    "threshold": threshold,
                    "timestamp": datetime.utcnow().isoformat()
                })
                # Keep only last 100 events
                if len(self._low_confidence_events) > 100:
                    self._low_confidence_events = self._low_confidence_events[-100:]
    
    def get_latency_stats(self, model_name: str) -> Dict[str, float]:
        """Get latency statistics for a model"""
        with self._lock:
            latencies = self._latencies.get(model_name, [])
            if not latencies:
                return {"count": 0}
            
            sorted_latencies = sorted(latencies)
            count = len(sorted_latencies)
            
            return {
                "count": count,
                "mean": sum(sorted_latencies) / count,
                "min": min(sorted_latencies),
                "max": max(sorted_latencies),
                "p50": sorted_latencies[int(count * 0.5)],
                "p95": sorted_latencies[int(count * 0.95)],
                "p99": sorted_latencies[int(count * 0.99)] if count > 100 else sorted_latencies[-1]
            }
    
    def get_prediction_counts(self, model_name: str = None) -> Dict:
        """Get prediction counts for a model or all models"""
        with self._lock:
            if model_name:
                return dict(self._prediction_counts.get(model_name, {"success": 0, "failure": 0}))
            return {k: dict(v) for k, v in self._prediction_counts.items()}
    
    def get_confidence_stats(self, model_name: str) -> Dict[str, float]:
        """Get confidence score statistics"""
        with self._lock:
            scores = self._confidence_scores.get(model_name, [])
            if not scores:
                return {"count": 0}
            
            return {
                "count": len(scores),
                "mean": sum(scores) / len(scores),
                "min": min(scores),
                "max": max(scores)
            }
    
    def get_low_confidence_events(self) -> List[Dict]:
        """Get recent low confidence prediction events"""
        with self._lock:
            return list(self._low_confidence_events)
    
    def get_all_metrics(self) -> Dict:
        """Get all collected metrics"""
        with self._lock:
            return {
                "latencies": {
                    model: self.get_latency_stats(model)
                    for model in self._latencies.keys()
                },
                "predictions": self.get_prediction_counts(),
                "confidence": {
                    model: self.get_confidence_stats(model)
                    for model in self._confidence_scores.keys()
                },
                "low_confidence_events": list(self._low_confidence_events)
            }


# Global metrics collector instance
metrics_collector = MetricsCollector()


class LatencyTimer:
    """Context manager for measuring latency"""
    
    def __init__(self, model_name: str, collector: MetricsCollector = None):
        self.model_name = model_name
        self.collector = collector or metrics_collector
        self.start_time = None
        self.latency_ms = None
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.latency_ms = (time.time() - self.start_time) * 1000
        self.collector.record_latency(self.model_name, self.latency_ms)
        return False
