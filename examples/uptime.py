"""
Calculates uptime in seconds, incrementing every counter_interval
"""
import time

from rhizome.lib.protocol import RhizomeProtocol

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--listen-addr', help='IP address for RhizomProtocol instance to listen on', default='0.0.0.0')
    parser.add_argument('--listen-port', help='Port for RhizomeProtocol instance to listen on', type=int, default=54322)
    parser.add_argument('--node-hostname', help='IP address for known Rhizome node', default='localhost')
    parser.add_argument('--node-port', help='Port known Rhizome node is listening on', type=int, default=54321)
    args = parser.parse_args()

    # Set up RhizomeProtocol
    rhizome = RhizomeProtocol(listen_hostname=args.listen_addr, listen_port=args.listen_port)
    rhizome.start(args.node_hostname, args.node_port)
    # Set up code to be run
    counter = 0
    counter_interval = 10
    last_update_time = time.monotonic()
    while True:
        if last_update_time + counter_interval > time.monotonic():
            time.sleep(last_update_time + counter_interval - time.monotonic())
        counter += counter_interval
        print(f"Uptime: {counter} seconds")
        last_update_time = time.monotonic()
