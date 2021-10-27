import os
import tarfile
import zipfile


def is_neglect_path(path, rules: list):
    def single_comp(path, rule):
        l = path.replace('\\', '/')
        l = l.split('/')
        if len(l) >= len(rule):
            for i, comp in enumerate(rule):

                if l[i] != comp:
                    return False
            return True
        else:
            return False

    for rule in rules:
        res = single_comp(path, rule)
        if res:
            return True
    return False

def unzip_file(zip_src: str, dst_dir: str):
    """
    解压文件
    Args:
        zip_src:
        dst_dir:

    Returns:

    """
    r = zipfile.is_zipfile(zip_src)
    if r:
        fz = zipfile.ZipFile(zip_src, 'r')
        for file in fz.namelist():
            fz.extract(file, dst_dir)
    else:
        print('This is not zip')


def make_zip(src_path, zip_dist_path, root='', rules=None):
    """
    创建zip包
    Args:
        src_path:
        zip_dist_path:
        root:
        rules:

    Returns:

    """
    if rules is None:
        rules = []
    z = zipfile.ZipFile(zip_dist_path, 'w', zipfile.ZIP_DEFLATED)
    for dirpath, dirnames, filenames in os.walk(src_path):
        relpath = os.path.relpath(dirpath, src_path)
        if is_neglect_path(relpath, rules):
            continue
        fpath = os.path.relpath(dirpath, src_path)
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            z.write(filepath, os.path.join(root, fpath , filename))
    z.close()


# 逐个添加文件打包，未打包空子目录。可过滤文件。
# 如果只打包不压缩，将"w:gz"参数改为"w:"或"w"即可。
def make_targz_one_by_one(zip_dist_path, src_path, rules):
    tar = tarfile.open(zip_dist_path, "w:gz")
    for dirpath, dir, files in os.walk(src_path):
        relpath = os.path.relpath(dirpath, src_path)

        if is_neglect_path(relpath, rules):
            continue
        if os.path.basename(dirpath) == '__pycache__':
            continue
        fpath = dirpath.replace(src_path, '')
        fpath = fpath and fpath + os.sep or ''
        for file in files:
            pathfile = os.path.join(dirpath, file)
            if relpath == '.':
                tar.add(pathfile, arcname=os.path.join('PyMiner', file))
            else:
                tar.add(pathfile, arcname=os.path.join('PyMiner', relpath, file))
            print('压缩文件:%s' % pathfile)
    tar.close()


if __name__ == '__main__':
    import time

    t0 = time.time()
    # 生成tar文件需要278s
    # 生成tar.gz需要...?
    make_zip(r'F:\transfer\PyminerExternalPlugins\mechanics',
             r'c:\users\12957\desktop\test_with_outer_folder.zip',
             root='')
    make_zip(r'F:\transfer\PyminerExternalPlugins\mechanics',
             r'c:\users\12957\desktop\test_without_outer_folder.zip',
             root='.')
    make_zip(r'F:\transfer\PyminerExternalPlugins\mechanics',
             r'c:\users\12957\desktop\test_with_specified_folder_name.zip',
             root='folder')
    t1 = time.time()
    print(t1 - t0)
