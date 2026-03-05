# Source - https://stackoverflow.com/a/52337115
# Posted by Piotr Jasiek
# Retrieved 2026-03-05, License - CC BY-SA 4.0

import time
import platform

if platform.system() == 'Windows':
    import psutil

    def get_bytes(t):
        counters = psutil.net_io_counters()
        if t == 'tx':
            return counters.bytes_sent
        return counters.bytes_recv
else:
    def get_bytes(t, iface='wlan0'):
        with open('/sys/class/net/' + iface + '/statistics/' + t + '_bytes', 'r') as f:
            data = f.read()
            return int(data)

while True:
    tx1 = get_bytes('tx')
    rx1 = get_bytes('rx')

    time.sleep(1)

    tx2 = get_bytes('tx')
    rx2 = get_bytes('rx')

    tx_speed = round((tx2 - tx1)/1000000.0, 4)
    rx_speed = round((rx2 - rx1)/1000000.0, 4)

    print("TX: %fMbps  RX: %fMbps" % (tx_speed, rx_speed))
