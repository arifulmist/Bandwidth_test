

import time
import platform
import os

if platform.system() == 'Windows':
    import psutil

    def get_bytes(t):
        counters = psutil.net_io_counters()
        if t == 'tx':
            return counters.bytes_sent
        return counters.bytes_recv
else:
    def get_default_iface():
        """Find the first active network interface (excluding loopback)."""
        net_dir = '/sys/class/net/'
        for iface in os.listdir(net_dir):
            if iface == 'lo':
                continue
            # Check if interface is up
            try:
                with open(os.path.join(net_dir, iface, 'operstate'), 'r') as f:
                    if f.read().strip() == 'up':
                        return iface
            except:
                pass
        # Fallback: return first non-loopback interface
        for iface in os.listdir(net_dir):
            if iface != 'lo':
                return iface
        return 'eth0'

    DEFAULT_IFACE = get_default_iface()
    print(f"Using network interface: {DEFAULT_IFACE}")

    def get_bytes(t, iface=None):
        if iface is None:
            iface = DEFAULT_IFACE
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
