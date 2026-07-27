import argparse
from .data import Settings

def bind_and_get_args(sett: Settings):
        parser = argparse.ArgumentParser(prog="wtf")
        parser.add_argument("-m", "--model", default=sett.Model, type=str,
                            help="Ollama model to use")
        parser.add_argument("-l", "--lines", default=1, type=int,     # this one is handled buy the bash runner. Not python.
                            help="How many previous commands to send to the model")
        parser.add_argument("-t", "--think", action="store_true", dest="think", default=sett.Think,
                            help="Enable advanced thinking")
        parser.add_argument("-nt", "--no-think", action="store_false", dest="think", default=sett.Think,
                            help="Disable advanced thinking")
        parser.add_argument("-d", "--debug", action="store_true", dest="debug", default=sett.Debug,
                            help="Include to show debug output")
        parser.add_argument("-v", "--version", action="store_true", dest="version", default=False,
                            help="Prints the version of the application")
        args = parser.parse_args()

        sett.Debug = args.debug
        sett.Model = args.model
        sett.Think = args.think
        #if (sett.Debug): print(f"args={args}")
        return args