
import os


from core.context.context_engine import ContextEngine

ce = ContextEngine()
print(ce.get_context("test"))