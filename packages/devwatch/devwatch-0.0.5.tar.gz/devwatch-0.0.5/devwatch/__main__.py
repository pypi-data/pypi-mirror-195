import argparse
from devwatch.devwatch import main


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("-t", "--target")
  argv = parser.parse_args()
  main(argv.target)
