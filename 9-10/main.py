import csv
import platform
import subprocess

# 10. Сначала руками в терминале, а затем скриптом на любом ЯП:
# Выполнить DNS-запросы для списка доменов.
# Сохранить их IP-адреса.
# Выполнить traceroute для каждого IP-адреса.
# Сохранить результаты в CSV-файл.


INPUT = "/Users/danielgehrman/Documents/Programming/Uni/Networking/9-10/domains.csv"
OUTPUT = "/Users/danielgehrman/Documents/Programming/Uni/Networking/9-10/traceroute_results.csv"

"""
traceroute to google.com (142.251.38.78), 64 hops max, 40 byte packets
 1  10.40.181.1  66.125 ms  28.482 ms  140.417 ms
 2  178.49.129.17  595.122 ms *  267.397 ms
 3  10.245.138.242  354.792 ms * *
 4  10.245.220.2  1019.441 ms  637.130 ms  81.939 ms
 5  10.245.220.1  218.900 ms  34.025 ms  11.875 ms
 6  178.49.128.50  196.010 ms  99.299 ms  220.041 ms
 7  * 188.234.152.203  319.474 ms  756.185 ms
 8  188.234.131.53  229.631 ms
    72.14.214.138  550.198 ms
    188.234.131.53  153.944 ms
 9  74.125.244.133  386.096 ms
    142.251.38.78  410.219 ms
    74.125.244.180  373.734 ms
"""

class Traceroute_result():
    def __init__(self, data:str):
        data_arrayed_with_ms_and_stars = [row.split() for row in data.split("\n")]
        data_arrayed_with_ms_and_stars.pop(-1)
        data_arrayed = [
            list(filter(lambda a: a != '*' and a != 'ms', row))   # https://stackoverflow.com/questions/1157106/
            for row in data_arrayed_with_ms_and_stars
        ]
        self.destinationDomain = data_arrayed[0][2]  # google.com
        self.destinationAddress = data_arrayed[0][3][1:-2]   # tipa 8.8.8.8
        self.hops = []  # each hop is an array of dicts (probes) [{'destinationIP': '', 'roundTripTimes': ''}]

        hop_number = 1
        for row in data_arrayed:
            # hop = {'destinationIP': '', 'roundTripTime': ''}
            hop = []
            probe = {'destinationIP': '', 'roundTripTimes': []}

            if row[0].isdigit():
                hop_number = int(row.pop(0))
                self.hops.append([])

            if row != []:

                probe['destinationIP'] = row.pop(0)
                probe['roundTripTimes'] = row
            
            hop.append(probe)

            self.hops[hop_number - 1].append(hop)

    def __str__(self):
        rows = []
        for i, hop in enumerate(self.hops, 1):
            columns = [str(i)]
            if not any(p for probe_list in hop for p in probe_list):
                columns += ['*', '*'] * 3  # 3 probes, each ip+time
            else:
                for probe_list in hop:
                    for p in probe_list:
                        for t in p['roundTripTimes']:
                            columns.extend([p['destinationIP'], t])
            rows.append(','.join(columns))
        return '\n'.join(rows)

    # def __str__(self):
    #     return '\n'.join([' '.join(temp) for temp in  temp_hop in self.hops])




def traceroute(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.

    Source - https://stackoverflow.com/a/32684938
    Posted by ePi272314, modified by community. See post 'Timeline' for change history
    Retrieved 2026-02-05, License - CC BY-SA 4.0
    """

    # param = '-n' if platform.system().lower()=='windows' else '-c'
    command = ['traceroute', '-n', host]
    return subprocess.run(command, capture_output=True).stdout.decode()


def get_domains_from_csv(filepath):
    data = []
    with open(filepath, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            data.append(row[0])
    return data


def write_result_to_csv(filepath, data, arg=['domain', 'ip', 'time', 'packetLoss']):

    with open(filepath, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(arg)

        for pinged_domain in data:
            row = [getattr(pinged_domain, i) for i in arg]

            # row = [
            #     pinged_domain.domain,
            #     pinged_domain.ip,
            #     pinged_domain.time,
            #     pinged_domain.packetLoss
            # ]

            spamwriter.writerow(row)


def main():
    domains = get_domains_from_csv(INPUT)
    ping_result = []

    print("hop,probe1_ip,time1,probe2_ip,time2,probe3_ip,time3")

    for domain in domains:
        if domain == 'domain':
            continue
        print(f"tracing {domain=}")

        return_data = traceroute(domain)
        result_data = Traceroute_result(return_data)

        print(result_data)

    #     pigned_domain_result = Ping_result(return_data)

    #     ping_result.append(pigned_domain_result)

    # write_result_to_csv(OUTPUT, ping_result)


if __name__ == "__main__":
    main()




# CompletedProcess(args=['ping', '-c', '1', 'google.com'],
#                  returncode=0,
#                  stdout=b'PING google.com (142.250.185.142): 56 data bytes\n64 bytes from 142.250.185.142: icmp_seq=0 ttl=64 time=0.339 ms\n\n--- google.com ping statistics ---\n1 packets transmitted, 1 packets received, 0.0% packet loss\nround-trip min/avg/max/stddev = 0.339/0.339/0.339/nan ms\n', stderr=b'')




' 1  10.0.1.1  19.836 ms  3.335 ms  4.139 ms\n 2  10.3.128.1  5.204 ms  3.817 ms  3.752 ms\n 3  84.237.49.114  4.692 ms  4.687 ms  129.316 ms\n 4  84.237.49.123  6.874 ms  3.470 ms  3.921 ms\n'