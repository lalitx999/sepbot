import sys
import copy

# Python 3.14 Compatibility Patch for Django Template Context Copying
if sys.version_info >= (3, 14):
    try:
        from django.template import context
        
        def _patched_context_copy(self):
            duplicate = object.__new__(self.__class__)
            for k, v in self.__dict__.items():
                if k == 'dicts':
                    duplicate.dicts = self.dicts[:]
                elif k == 'render_context':
                    duplicate.render_context = copy.copy(self.render_context)
                else:
                    setattr(duplicate, k, v)
            return duplicate

        context.BaseContext.__copy__ = _patched_context_copy
        context.Context.__copy__ = _patched_context_copy
        context.RequestContext.__copy__ = _patched_context_copy
    except Exception as e:
        print(f"Python 3.14 patch warning: {e}")

from .celery import app as celery_app

__all__ = ('celery_app',)
