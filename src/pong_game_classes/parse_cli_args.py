import argparse

class GameArgs(argparse.Namespace):
    difficulty: str
    mode: str
    enable_sounds: str

parser = argparse.ArgumentParser()
parser.add_argument("--difficulty", choices=["easy", "hard"], default="easy", help="Game difficulty selection")
parser.add_argument("--mode", choices=["ai", "2p"], default="ai", help="Game difficulty selection")
parser.add_argument("--enable_sounds", choices=["0", "1"], default="0", help="Flag to enable turn on/off sound-effects")

CLI_ARGS = parser.parse_args(namespace=GameArgs())