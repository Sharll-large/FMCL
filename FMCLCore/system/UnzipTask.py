import zipfile


def unzip(path, topath):
    zip_file = zipfile.ZipFile(path)
    for names in zip_file.namelist():
        zip_file.extract(names, topath)
