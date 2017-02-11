import operator
import itertools
import psutil 


conn_list = psutil.net_connections(kind = 'inet')    # Get the net connections data from PSUTIL
sort_list = []
valid_conn_list = []

# Remove the invalid connection data i.e records without laddr / raddr / status = NONE
for connections in conn_list:
    if connections.laddr and connections.raddr and connections.status is not 'NONE':
        valid_conn_list.append(connections)

# Groupby the connection list by pid and maintaining a dict to store the
# no. of connections per process(pid)
for key, group in itertools.groupby(valid_conn_list, key=lambda x:x[6]):
     dict_conn = dict({"pid":key, "length":len(list(group))})
     sort_list.append(dict_conn)

# Sort by no of connections per process (Descending Order)
sort_list.sort(key=operator.itemgetter('length'), reverse=True)

# Print header
print '"pid","laddr","raddr","status"'

# Print data
for Conn in sort_list:
    for ConnObj in valid_conn_list:
        if ConnObj.pid == Conn['pid']:
            laddress = "%s@%d" %ConnObj.laddr
            raddress = "%s@%s" %ConnObj.raddr
            print '"%d","%s","%s","%s"' %(ConnObj.pid, laddress, raddress, ConnObj.status)
