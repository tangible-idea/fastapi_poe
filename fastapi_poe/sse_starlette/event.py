"""
Compatibility module for sse_starlette.

This module provides the ServerSentEvent class which is imported in the base.py file
but might not be directly available in the installed sse_starlette package.
"""

from sse_starlette.sse import ServerSentEvent
