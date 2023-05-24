import argparse

def setup_and_parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int)
    return parser.parse_args()
