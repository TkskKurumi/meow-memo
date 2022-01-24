from . import files
import time
from . import algorithms
from . import ioutil
subcommands = dict()


def deco(func):
    subcommands[func.__name__] = func


@deco
def help(argdict):
    print("meow add [key] [value]")
    print("    to add (overwrite) [key] 's memo ")
    print("meow app [key] [value]")
    print("    to append a line to the end of  [key] 's memo")  # nopep8
    print("meow edit [key]")
    print("    to open an editor for [key], tool will try invoke vscode, nano, gvim.")    # nopep8
    print("meow [key]")
    print("    to search memo for key")


def update_data(key, value):
    files.datas[key] = value
    files.times[key] = time.time()


def do_search(key, first=0.2):
    key_len = len(key)
    results = []
    for k, v in files.datas.items():
        common = algorithms.lcs(key, k)
        # v_common_len, v_common_str = algorithms.lcs(key, v)

        score = common.common_ratio
        results.append((score, k, v, common))
    results.sort(key=lambda x: -x[0])    # sort by score descending
    sum_score = sum([x[0] for x in results])*first
    for idx, i in enumerate(results):
        score, k, v, common = i
        colored_key, colored_k = common.color_common()
        print(colored_key, "->", colored_k, ":")

        for i in v.split("\n"):
            print("    ", i, sep="")
        sum_score -= score
        if(sum_score < 0):
            break
    return


@deco
def edit(argdict):
    _args = argdict.get("positional")
    cmd = _args[0]  # "edit"
    key = _args[1]  # key
    if(key in files.datas):
        value = files.datas[key]
    else:
        value = None
    value = ioutil.input_with_editor(value)
    update_data(key, value)
    do_search(key, first=0)


@deco
def add(argdict):
    _args = argdict.get("positional")
    cmd = _args[0]    # "add"
    key = _args[1]    # key
    value = _args[2]  # value
    update_data(key, value)
    do_search(key, first=0)


@deco
def app(argdict):
    _args = argdict.get("positional")
    cmd = _args[0]   # "app"
    key = _args[1]   # key
    value = _args[2]  # value
    v = files.datas.get(key, "")
    if(v):
        v = v+"\n"+value
    else:
        v = value
    update_data(key, v)
    do_search(key, first=0)


@deco
def search(argdict):
    _args = argdict.get("positional")
    key = " ".join(_args)
    do_search(key)