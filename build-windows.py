import PyInstaller.__main__

APP_NAME = "Gucker"

PyInstaller.__main__.run([
    'entrypoint.py',
    '--clean',
    # '--windowed',
    f'--name={APP_NAME}',
    '--noconfirm',
    '--additional-hooks-dir=hooks',
])