import os
import re

from genericpath import isfile


def cut_string(string: str, part_len: int):
    return list(string[0 + i: part_len + i] for i in range(0, len(string), part_len))


def get_all_cogs():
    """Returns all available cogs with their class names as ordered dict."""
    all_cogs = {}
    pattern = r"class (.*)\(commands\.Cog\):"
    for name in os.listdir("./cogs"):
        filename = f"./cogs/{name}"
        if isfile(filename) and filename.endswith(".py"):
            with open(filename, "r") as file:
                for line in file:
                    if re.search(pattern, line):
                        result = re.search(pattern, line)
                        all_cogs[name[:-3]] = result.group(1)
                        break
    return {key: all_cogs[key] for key in sorted(all_cogs.keys())}


def split(array, k):
    """Splits list into K parts"""
    n = len(array)
    lists = [array[i * (n // k) + min(i, n % k):(i+1) * (n // k) + min(i+1, n % k)] for i in range(k)]
    return lists


def create_bar(value, total) -> str:
    prog_bar_str = ""
    prog_bar_length = 10
    percentage = 0
    if total != 0:
        percentage = value / total
        for i in range(prog_bar_length):
            if round(percentage, 1) <= 1 / prog_bar_length * i:
                prog_bar_str += "░"
            else:
                prog_bar_str += "▓"
    else:
        prog_bar_str = "░" * prog_bar_length
    prog_bar_str = prog_bar_str + f" {round(percentage * 100)}%"
    return prog_bar_str
