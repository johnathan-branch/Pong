import argparse

class GameArgs(argparse.Namespace):
    difficulty: str
    mode: str

parser = argparse.ArgumentParser()
parser.add_argument("--difficulty", choices=["easy", "hard"], default="easy", help="Game difficulty selection")
parser.add_argument("--mode", choices=["ai", "2p"], default= "ai", help="Game difficulty selection")

CLI_ARGS = parser.parse_args(namespace=GameArgs())