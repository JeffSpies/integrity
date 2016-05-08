
def get_checksums(filename, algos, chunk_size=8096*2):
    results = {}
    classes = {}

    for key, value in algos.items():
        classes[key] = value()

    with open(filename, 'rb') as f:
        while True :
            d = f.read(chunk_size)
            if not d:
                break
            for key, value in classes.items():
                value.update(d)

    for key, value in classes.items():
        results[key] = value.hexdigest()

    return results


def get_checksum(filename, algo, chunk_size=8096*2):
    m = algo()
    with open(filename, 'rb') as f:
        while True :
            d = f.read(chunk_size)
            if not d:
                break
            m.update(d)
    d = m.hexdigest()
    return d
