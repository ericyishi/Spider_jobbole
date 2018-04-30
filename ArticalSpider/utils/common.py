import hashlib


def get_md5(url):
    # 因为python3，默认的编码是Unicode，但是get_md5传入需要utf-8所以需要编码
    # 如果url是字符串（字符串默认是Unicode）【python2中有关键字unicode】那么就转码
    if isinstance(url, str):
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()