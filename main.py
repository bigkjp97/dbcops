import threading
import yaml
import argparse

from prometheus_client import start_http_server

from utils.oracleSql import oracleSQL


def main():
    parser = argparse.ArgumentParser()
    # 设置传参方式
    parser.add_argument('-f', '--file', default='./init.yml')
    args = parser.parse_args()
    with open(args.file, 'r') as conf:
        c = yaml.load(conf, Loader=yaml.FullLoader)

    # print(configSet)
    start_http_server(int(c['server']['port']), c['server']['host'])
    client = c['server']['instantclient']
    for config in c['config']:
        o = threading.Thread(target=oracleSQL(config, client).do_execute())
        o.start()
    # for case in cases:
    #     file = case['file']
    #     job = case['job']
    #     keywords = case['keywords']
    #     label = case['label']
    #     # 开启多线程
    #     t = threading.Thread(target=tail.Tail(file, job, keywords, label, pushHost,hostName).tail)
    #     t.start()
    #     # threads.append(t)


if __name__ == '__main__':
    main()
