"""Shared settings entry-point for MLOps scripts."""

from apps.api.config.settings import AppSettings, get_settings

__all__ = ["AppSettings", "get_settings"]
