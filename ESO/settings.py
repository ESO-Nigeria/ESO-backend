"""
Django settings for ESO project.

Generated by 'django-admin startproject' using Django 5.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-y^wd)qhlp!%b_0xqu@h&wn4r@nvsqm0pt12+h*0^!jnewt_vs5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    # 'admin_soft.apps.AdminSoftDashboardConfig',
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'ESOapp',
    'djoser',
    'rest_framework',
    'rest_framework.authtoken',
]


CORS_ALLOW_ALL_ORIGINS = True

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.zoho.com'
EMAIL_PORT = 587
EMAIL_HOST_PASSWORD = 'PceYVPHcLSZf'
EMAIL_HOST_USER = 'support@kedak.site'
EMAIL_USE_SSL = False
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL='support@kedak.site'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'ESO.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ESO.wsgi.application'


JAZZMIN_SETTINGS = {
    "site_title": "ESO Nigeria Admin",
    "site_header": "ESO Nigeria Administration",
    "site_brand": "ESO Nigeria",
    "welcome_sign": "Welcome to ESO Nigeria Admin",
    "copyright": "ESO Nigeria 2024",
    "search_model": "auth.User",
    "show_ui_builder": True,
    "show_settings": True,
    "topmenu_links": [
        {"name": "Dashboard", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "ESO Nigeria", "url": "https://esonigeria.com", "new_window": True},
    ],
     "icons": {
        "auth.user": "far fa-user",
        "auth.Group": "far fa-users",
        "ESOapp.CustomUser": "far fa-user",
        
        # Communication
        "ESOapp.AdminNotification": "far fa-envelope",
        "ESOapp.Notification": "far fa-bell",
        "ESOapp.Comment": "far fa-comments",
        
        # Settings & Configuration
        "ESOapp.Setting": "far fa-cog",
        "ESOapp.Program": "far fa-calendar",
        
        "ESOapp.Profile": "far fa-building",
        "AuthToken.Token": "far fa-key",
    }
}


JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": False,
    "accent": "accent-teal",
    "navbar": "navbar-white navbar-light",
    "no_navbar_border": True,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": True,
    "sidebar_fixed": True,
    "sidebar": "sidebar-light-olive",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "lux",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-outline-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    },
    "custom_css": '/static/css/custom.css',
    "custom_js": None
}

DJOSER = {
'LOGIN_FIELD': 'email',
"DOMAIN": "https://esonigeria.com",
'SITE_NAME':'ESO Nigeria',
'HIDE_USERS':False,
"USERNAME_FIELD": "email", 
'USER_CREATE_PASSWORD_RETYPE': True,
'USERNAME_CHANGED_EMAIL_CONFIRMATION': True,
'PASSWORD_CHANGED_EMAIL_CONFIRMATION': True,
'SEND_CONFIRMATION_EMAIL': True,
# 'SET_USERNAME_RETYPE': True,
'SET_PASSWORD_RETYPE': False,
'PASSWORD_RESET_CONFIRM_URL': 'password/reset/confirm/{uid}/{token}',
'USERNAME_RESET_CONFIRM_URL': 'email/reset/confirm/{uid}/{token}',
'ACTIVATION_URL': 'activate/{uid}/{token}',
'SEND_ACTIVATION_EMAIL': True,

'SERIALIZERS': {
'user_create': 'ESOapp.serializers.CustomUserCreateSerializer',
'user': 'ESOapp.serializers.CustomUserCreateSerializer',
'current_user': 'ESOapp.serializers.CustomUserCreateSerializer',
'user_delete': 'djoser.serializers.UserDeleteSerializer',
'token_create': 'djoser.serializers.TokenCreateSerializer',
},
'EMAIL':{
'activation': 'djoser.email.ActivationEmail',
'confirmation': 'djoser.email.ConfirmationEmail',
'password_reset': 'djoser.email.PasswordResetEmail',
'password_changed_confirmation': 'djoser.email.PasswordChangedConfirmationEmail',
'username_changed_confirmation': 'djoser.email.UsernameChangedConfirmationEmail',
'username_reset': 'djoser.email.UsernameResetEmail',
},
'PERMISSIONS': {
        'user': ['rest_framework.permissions.IsAuthenticatedOrReadOnly'],
    }
}

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)



# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'NON_FIELD_ERRORS_KEY': 'error',
}




# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
AUTH_USER_MODEL = 'ESOapp.CustomUser'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'