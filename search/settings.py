"""App specific settings"""

from django.conf import settings

if hasattr(settings, 'FEATURES'):
    IS_USING_TAXOMAN = settings.FEATURES.get('ENABLE_TAXOMAN', False)
else:
    IS_USING_TAXOMAN = False
