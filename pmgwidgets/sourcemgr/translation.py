def create_translation(target_files: str):
    import os
    folder = os.path.dirname(target_files)
    name = os.path.basename(target_files)
    name_without_ext = os.path.splitext(name)
    names = ''
    for file_path in target_files:
        name = os.path.basename(file_path)
        names += name + ' '
    os.system('cd %s && pylupdate5 -noobsolete %s -ts translations/%s.ts' % (folder, names, name_without_ext))
