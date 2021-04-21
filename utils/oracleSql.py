from time import sleep

from prometheus_client import Gauge

import cx_Oracle


class oracleSQL:
    def __init__(self, config):
        self._database = config['database']
        self._sqlText = config['sqltext']
        self._matric = config['matric']
        self._tag = config['tag']
        self._label = config['label']
        self._interval = config['interval']
        self._gauge = Gauge('dbcops_' + self._tag + '_' + self._matric, 'Return value of column ' + self._matric,
                            self._label)

    def fetch_table(self, cursor, sql):
        # count index
        global valIndex
        index = 0
        labIndex = []
        cursor.execute(sql)
        # (name, type, display_size, internal_size, precision, scale, null_ok)
        # read every column
        for column in cursor.description:
            # VARCHAR and NOT NULL
            if column[0] in self._label:
                if column[6] != 0 and (column[1] != cx_Oracle.DB_TYPE_VARCHAR or column[1] != cx_Oracle.DB_TYPE_CHAR):
                    raise KeyError("The label '" + column[0] + "' is not suitable, make sure it's not null and char")
                labIndex.append(index)
            # collect NUMBER data
            if column[0] == self._matric:
                if column[1] != cx_Oracle.DB_TYPE_NUMBER:
                    raise ValueError("Value of this matric is not NUMBER")
                # NUMBER column's index
                valIndex = index
            index += 1
        # numColIndex matches matrics
        # g = GaugeMetricFamily('dbcops_' + self._matric, 'Return value of column ' + self._matric, self._label)
        # fetch data from each row and collect with matric
        for row in cursor:
            tupLab = []
            for l in range(len(self._label)):
                tupLab.append(row[labIndex[l]])
            self._gauge.labels(*tupLab).set(row[valIndex])
            # g.add_metric(*tupLab, row[2])
            # g.set(row[numColIndex[i]])

    def do_execute(self):
        # build connection
        while True:
            with cx_Oracle.connect(self._database) as conn:
                with conn.cursor() as cur:
                    self.fetch_table(cur, self._sqlText)
            sleep(self._interval * 60)
