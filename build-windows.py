import PyInstaller.__main__
import shutil 


APP_NAME = "Gucker"

PyInstaller.__main__.run([
    'entrypoint.py',
    '--clean',
    '--windowed',
    "--onedir",
    f'--name={APP_NAME}',
    '--noconfirm',
    '--additional-hooks-dir=hooks',
])

shutil.make_archive("./dist/GuckerApp", "zip", "./dist/Gucker")
print("Made archive")