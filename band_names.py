from .hdf5_getters import get_artist_name, get_year, open_h5_file_read
import json
import pandas as pd


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
    s = {k: v for k, v in s.items() if len(v) > 0}
    s = {k: [int(i) for i in v] for k, v in s.items()}
    return s


def save(root):
    summary = build_summary(root, limit=None)
    s2 = convert(summary)
    with open("summary.json", "w") as f:
        json.dump(s2, f, indent=2)


def main():
    with open("summary.json") as f:
        s2 = json.load(f)
    s3 = {k: sorted(v)[0] for k, v in s2.items()}
    df = pd.DataFrame({"artist": s3.keys(), "year": s3.values()})
    df["label"] = df.artist.str.startswith("The")
    df.label = df.label.apply(lambda b: "the" if b else "no_the")
    df.hist(column="year", by="label")
