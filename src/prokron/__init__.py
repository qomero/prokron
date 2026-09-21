"""Prokron: a repository-native project cognition layer.

The authored Markdown under `prokron/` is the only source of truth. This
package compiles it into derived state under `.prokron/` and answers questions
about it deterministically, with no model provider in the loop.
"""

from .cli import VERSION, main

__version__ = VERSION
__all__ = ["VERSION", "main"]
