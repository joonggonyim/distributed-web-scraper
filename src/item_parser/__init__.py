import os

__all__ = [f.strip('.py') for f in os.listdir(os.path.dirname(__file__)) 
           if not f.startswith('__')]