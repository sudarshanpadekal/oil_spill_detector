import pathlib
p = pathlib.Path(r'C:\Users\ABCDE\AppData\Local\Programs\Python\Python311\Lib\site-packages\ultralytics\cfg\__init__.py')
lines = p.read_text(errors='ignore').splitlines()
for i,l in enumerate(lines,1):
    if 'def get_save_dir' in l or i in range(380, 460):
        pass
for i in range(380, 460):
    print(f'{i}: {lines[i-1]}')
