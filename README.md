# dbcops

## purpose

I made this program for the purpose of monitoring tables of database. For some cases, we may want to fetch value of some
columns in a table, this requirement needs flexibility, likes we can use some column value(which is in varchar or char
type) as labels and focus on monitoring numerical value.

### init.yml
```yaml
server:
  host: 'localhost'
  port: '9093'
  instantclient: ''
config:
  # usr/passwd@host:1521/db
  - database: ''
    # query
    sqltext: ""
    # matrics: which column needs to be collected(NUMBER)
    matric: ''
    # label: column name(not null)
    label: [ '' ]
    # minute
    interval: 1
```
## run
```shell
tar zxvf dbcops-linux.tar.gz
cd dbcops
# start program
./dbcops -f init.yml
```