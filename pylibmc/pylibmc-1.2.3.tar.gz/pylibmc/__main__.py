"""Interactive shell"""

import sys
import code
import random
import pylibmc

tips = [
    "Want to use 127.0.0.1? Just hit Enter immediately.",
    "This was supposed to be a list of tips but I...",
    "I don't really know what to write here.",
    "Really, hit Enter immediately and you'll connect to 127.0.0.1.",
    "Did you know there's a --binary flag? Try it!",
    "Want to use binary mode? Pass --binary as a sole argument."
]

def print_header(outf=sys.stdout):
    outf.write("pylibmc interactive shell\n\n")
    outf.write("Input list of servers, terminating by a blank line.\n")
    outf.write(random.choice(tips) + "\n")

def collect_servers():
    in_addr = raw_input("Address [127.0.0.1]: ")
    if in_addr:
        while in_addr:
            yield in_addr
            in_addr = raw_input("Address [<stop>]: ")
    else:
        yield "127.0.0.1"

banner = "\nmc client available as `mc`\n"
def interact(servers, banner=banner, binary=False):
    mc = pylibmc.Client(servers, binary=binary)
    local = {"pylibmc": pylibmc,
             "mc": mc}
    code.interact(banner=banner, local=local)

def main():
    binary = False
    if sys.argv[1:] == ["--binary"]:
        binary = True
    print_header()
    interact(list(collect_servers()), binary=binary)

if __name__ == "__main__":
    main()
