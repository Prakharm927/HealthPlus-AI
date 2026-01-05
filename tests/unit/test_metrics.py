"""
Unit tests for metrics collection
"""

import pytest
from src.monitoring.metrics import MetricsCollector, LatencyTimer


@pytest.mark.unit
def test_metrics_collector_latency():
    """Test latency recording"""
    collector = MetricsCollector()
    collector.record_latency("test_model", 100.0)
    collector.record_latency("test_model", 150.0)
    
    stats = collector.get_latency_stats("test_model")
    assert stats["count"] == 2
    assert stats["mean"] == 125.0
    assert stats["min"] == 100.0
    assert stats["max"] == 150.0


@pytest.mark.unit
def test_metrics_collector_predictions():
    """Test prediction counting"""
    collector = MetricsCollector()
    collector.record_prediction("test_model", True)
    collector.record_prediction("test_model", True)
    collector.record_prediction("test_model", False)
    
    counts = collector.get_prediction_counts("test_model")
    assert counts["success"] == 2
    assert counts["failure"] == 1


@pytest.mark.unit
def test_metrics_collector_confidence():
    """Test confidence tracking"""
    collector = MetricsCollector()
    collector.record_confidence("test_model", 0.9, 0.75)
    collector.record_confidence("test_model", 0.6, 0.75)
    
    stats = collector.get_confidence_stats("test_model")
    assert stats["count"] == 2
    assert stats["mean"] == 0.75
    
    # Check low confidence events
    low_conf_events = collector.get_low_confidence_events()
    assert len(low_conf_events) >= 1


@pytest.mark.unit
def test_latency_timer():
    """Test latency timer context manager"""
    collector = MetricsCollector()
    
    with LatencyTimer("test_model", collector) as timer:
        pass
    
    assert timer.latency_ms is not None
    assert timer.latency_ms >= 0
    
    stats = collector.get_latency_stats("test_model")
    assert stats["count"] == 1
