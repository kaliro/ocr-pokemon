import glob
import itertools
import os
import shlex
import sys
import subprocess
import pandas as pd


def check_tesseract():
    """Returns true if tesseract is found, else False"""
    try:
        subprocess.run("which tesseract", shell=True)
    except Exception:
        return False
    return True


def sanity_check(dirname):
    """Check if tesseract is available, check if input directory is available
    """
    if not check_tesseract():
        print("tesseract is not available, exiting")
        sys.exit(1)

    if not os.path.isdir(dirname):
        print("Directory {} does not exist".format(dirname))
        sys.exit(2)


def turn_to_pandas_df(lines):
    pokemons, cps, times, modes = [], [], [], []
    lines = list(itertools.chain(*[l.strip().split("\n") for l in lines]))
    for i in range(len(lines)):
        line = lines[i]
        if line.endswith("was caught!"):
            pokemons.append(line.split()[0])
            cps.append(int(lines[i + 2].replace("CP", "")))
            times.append(lines[i + 3].strip())
            modes.append("caught")
            i += 3
        elif line.endswith("was hatched!"):
            pokemons.append(line.split()[0])
            cps.append(int(lines[i + 2].replace("CP", "")))
            times.append(lines[i + 3].strip())
            modes.append("hatched")
            i += 3
    df = pd.DataFrame({"name": pokemons, "CP": cps, "datetime": times, "mode": modes})
    return(df)

def main(dirname):
    sanity_check(dirname)
    img_files = glob.glob(os.path.join(dirname, "*.png"))
    output = []
    for fname in img_files:
        proc = subprocess.run(shlex.split("tesseract {} stdout".format(fname)), stdout=subprocess.PIPE)
        output.append(proc.stdout.decode('utf-8'))
    df = turn_to_pandas_df(output)
    df["datetime"] = pd.to_datetime(df["datetime"])
    df_sorted = df.drop_duplicates().sort_values(by="datetime")
    print(df_sorted)
    return df_sorted


if __name__ == "__main__":
    if not len(sys.argv) == 2:
        print("Usage: ")
    main(sys.argv[1])