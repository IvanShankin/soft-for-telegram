# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['app/start.py'],
    pathex=['G:\\clear_PyCharm_project\\black_smm_clear'],
    binaries=[],
    datas=[
	# Основные папки проекта           
        ('app/accounts/*.py', 'accounts'),
        ('app/accounts/ui/*.py', 'accounts/ui'),
        ('app/accounts/views/*.py', 'accounts/views'),
        
        ('app/convert/ui/*.py', 'convert/ui'),
        ('app/convert/views/*.py', 'convert/views'),
        
        ('app/create_bot/ui/*.py', 'create_bot/ui'),
        ('app/create_bot/views/*.py', 'create_bot/views'),

	('app/create_channel/ui/*.py', 'create_channel/ui'),
        ('app/create_channel/views/*.py', 'create_channel/views'),
        
        ('app/general/*.py', 'general'),
        ('app/general/ui/*.py', 'general/ui'),
        ('app/general/views/*.py', 'general/views'),
        
        ('app/invite/ui/*.py', 'invite/ui'),
        ('app/invite/views/*.py', 'invite/views'),
        
	('app/mailing_by_chats/ui/*.py', 'mailing_by_chats/ui'),
        ('app/mailing_by_chats/views/*.py', 'mailing_by_chats/views'),

        ('app/mailing_by_users/ui/*.py', 'mailing_by_users/ui'),
        ('app/mailing_by_users/views/*.py', 'mailing_by_users/views'),
        
        ('app/parser/ui/*.py', 'parser/ui'),
        ('app/parser/views/*.py', 'parser/views'),
        
        ('app/proxy/ui/*.py', 'proxy/ui'),
        ('app/proxy/views/*.py', 'proxy/views') 
	],
    hiddenimports=[
    # Основные модули проекта
    'accounts',
    'accounts.ui',
    'accounts.views',
        
    'convert.ui',
    'convert.views',

    'create_bot.ui',
    'create_bot.views',
        
    'create_channel.ui',
    'create_channel.views',
        
    'general',
    'general.ui',
    'general.views',
        
    'invite.ui',
    'invite.views',

    'mailing_by_chats.ui',
    'mailing_by_chats.views',        

    'mailing_by_users.ui',
    'mailing_by_users.views',
        
    'parser.ui',
    'parser.views',
        
    'proxy.ui',
    'proxy.views',
        
    # Внешние зависимости (оставьте ваш текущий список)
    'aiohappyeyeballs',
    'aiohttp',
    'aiohttp_socks',
    'aiosignal',
    'attrs',
    'bs4',
    'beautifulsoup4',
    'Brotli',
    'certifi',
    'charset_normalizer',
    'colorama',
    'frozenlist',
    'idna',
    'imagehash',
    'inflate64',
    'multidict',
    'multivolumefile',
    'numpy',
    'opentele',
    'phonenumbers',
    'PIL',
    'propcache',
    'psutil',
    'py7zr',
    'pyaes',
    'pyasn1',
    'pybcj',
    'Crypto',
    'pygame',
    'pyppmd',
    'PyQt5',
    'PyQt5.QtCore',
    'PyQt5.QtGui',
    'PyQt5.QtWidgets',
    'PySocks',
    'python_socks',
    'pytz',
    'pywt',
    'pyzstd',
    'rarfile',
    'requests',
    'rsa',
    'scipy',
    'socks',
    'soupsieve',
    'telethon',
    'texttable',
    'tgcrypto',
    'typing_extensions',
    'urllib3',
    'yarl'
],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='start',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
