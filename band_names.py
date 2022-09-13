from .hdf5_getters import get_artist_name, get_year, open_h5_file_read


def build_summary(root, limit=100):
    result = {}
    files = root.walk.files()
    files = list(files)[:limit]
    for f in files:
        path = root.getsyspath(f)
        h5 = open_h5_file_read(path)
        artist = get_artist_name(h5)
        year = get_year(h5)
        h5.close()
        if artist in result:
            result[artist].add(year)
        else:
            result[artist] = {year}
    return result


def convert(s):
    s = {k.decode(): v - {0} for k, v in s.items() if v != 0}
    s = {k: [int(i) for i in v] for k, v in s.items()}
    return s
