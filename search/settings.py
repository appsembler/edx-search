from django.conf import settings

print('edx-search settings.py called')

# IS_USING_TAXOMAN = is_using_taxoman()

# def is_using_taxoman():

#     if hasattr(settings, 'FEATURES'):
#         return settings.FEATURES.get('ENABLE_TAXOMAN', False)
#     else:
#         return False


if hasattr(settings, 'FEATURES'):
    IS_USING_TAXOMAN = settings.FEATURES.get('ENABLE_TAXOMAN', False)
else:
    IS_USING_TAXOMAN = False
