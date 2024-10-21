REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),

    'DEFAULT_PERMISSION_CLASSES': [
        'core.permissions.is_superuser_permission.IsSuperUser',
    ],

    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ],

    'DEFAULT_PAGINATION_CLASS': 'core.paginations.PagePagination',

    'EXCEPTION_HANDLER': 'core.handlers.error_handler.error_handler',

}
