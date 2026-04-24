"""
AI analysis package for ResourceMonitor.

Provides deterministic AI-style operational analysis and prompt templates
for future LLM integration.
"""

from .analyzer import AIEnhancedAnalyzer, save_ai_report

__all__ = ["AIEnhancedAnalyzer", "save_ai_report"]