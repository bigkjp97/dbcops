import threading
import yaml
import argparse

from cx_Oracle import init_oracle_client
from prometheus_client import start_http_server

from utils.oracleSql import oracleSQL


def main():
    parser = argparse.ArgumentParser()
    # parameter from system
    parser.add_argument('-f', '--file', default='./init.yml')
    args = parser.parse_args()
    with open(args.file, 'r') as conf:
        c = yaml.load(conf, Loader=yaml.FullLoader)

    # print(configSet)
    init_oracle_client(
        lib_dir=c['server']['instantclient'])
    start_http_server(int(c['server']['port']), c['server']['host'])
    for config in c['config']:
        # print(config)
        o = threading.Thread(target=oracleSQL(config).do_execute)
        o.start()


if __name__ == '__main__':
    main()
