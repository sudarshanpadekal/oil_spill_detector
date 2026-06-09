import ultralytics, pathlib
base = pathlib.Path(ultralytics.__file__).parent
for p in base.rglob('*.py'):
    txt = p.read_text(errors='ignore')
    if 'def get_save_dir' in txt:
        print('\nFILE', p)
        for i, l in enumerate(txt.splitlines(), 1):
            if 'def get_save_dir' in l:
                print('LINE', i)
                break
