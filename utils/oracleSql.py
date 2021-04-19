from time import sleep

from prometheus_client import Gauge

import cx_Oracle


class oracleSQL:
    def __init__(self, config):
        self._database = config['database']
        self._sqlText = config['sqltext']
        self._interval = config['interval']

    @staticmethod
    def fetch_table(cursor, sql):
        labIndex = []
        label = []
        # matrics名
        matrics = []
        # 下标计数
        index = 0
        # 存储数值类型列的下标
        numColIndex = []
        cursor.execute(sql)
        # (name, type, display_size, internal_size, precision, scale, null_ok)
        # 读取每列的数据类型及名称
        for column in cursor.description:
            print(column)
            # 符合varchar且不能为空的值作为label
            if column[1] == cx_Oracle.DB_TYPE_VARCHAR:
                label.append(column[0])
                labIndex.append(index)
            # 符合number类型即为需要采集的数值
            if column[1] == cx_Oracle.DB_TYPE_NUMBER:
                matrics.append(column[0])
                # 添加下标
                numColIndex.append(index)
            # 下标右移
            index += 1
        # numColIndex和matrics对应
        for i in range(len(numColIndex)):
            g = Gauge('dbcop_' + matrics[i], 'Return value of column ' + matrics[i], label)
            # 逐行获取对应列的值并采集到matrics
            for row in cursor:
                tupLab = []
                for l in range(len(label)):
                    tupLab.append(row[labIndex[l]])
                g.labels(*tupLab)
                # g.set(row[numColIndex[i]])

    def do_execute(self):
        # 建立连接
        cx_Oracle.init_oracle_client(
            lib_dir=r"C:\Users\BIGKJP97\PycharmProjects\dbcop\instantclient\instantclient_11_2")
        while True:
            with cx_Oracle.connect(self._database) as conn:
                with conn.cursor() as cur:
                    # 逐条执行sql
                    for sql in self._sqlText:
                        self.fetch_table(cur, sql)
            sleep(self._interval * 60)
