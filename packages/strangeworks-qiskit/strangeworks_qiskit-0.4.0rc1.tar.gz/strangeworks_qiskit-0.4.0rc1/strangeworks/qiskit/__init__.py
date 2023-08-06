"""Strangeworks Qiskit SDK"""
import importlib.metadata

import strangeworks

from .jobs.strangeworksjob import StrangeworksJob
from .provider import StrangeworksProvider, get_backend


__version__ = importlib.metadata.version("strangeworks-qiskit")
