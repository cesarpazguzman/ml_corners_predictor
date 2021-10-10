

def get_number(_string: str) -> int:
    try:
        return int(_string)
    except:
        return 90


def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))


def time_to_double(time_match: str) -> float:
    hours = float(time_match.split(":")[0])

    return hours + float(time_match.split(":")[1])/60.0
