# 1. Пингануть 10 доменов, вывести результаты в csv таблице.
# в качестве результатов предоставить RTT и 3 других параметра на ваше усмотрение

import csv
import platform
import subprocess


INPUT = "/Users/danielgehrman/Documents/Programming/Uni/Networking/1/domains.csv"
OUTPUT = "/Users/danielgehrman/Documents/Programming/Uni/Networking/1/ping_results.csv"

class Ping_result():
    def __init__(self, data:str):
        #закройте глаза
        dataArrayed = data.split()
        self.domain = dataArrayed[1]
        self.ip = dataArrayed[2][1:-2]
        self.time = dataArrayed[12].split("=")[-1]
        self.packetLoss = dataArrayed[25]
        self.allData = dataArrayed
        #можно открыть глаза


def ping(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.

    Source - https://stackoverflow.com/a/32684938
    Posted by ePi272314, modified by community. See post 'Timeline' for change history
    Retrieved 2026-02-05, License - CC BY-SA 4.0
    """

    param = '-n' if platform.system().lower()=='windows' else '-c'
    command = ['ping', param, '1', host]
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

    for domain in domains:
        if domain == 'domain':
            continue
        return_data = ping(domain)

        pigned_domain_result = Ping_result(return_data)

        ping_result.append(pigned_domain_result)

    write_result_to_csv(OUTPUT, ping_result)


if __name__ == "__main__":
    main()




# CompletedProcess(args=['ping', '-c', '1', 'google.com'],
#                  returncode=0,
#                  stdout=b'PING google.com (142.250.185.142): 56 data bytes\n64 bytes from 142.250.185.142: icmp_seq=0 ttl=64 time=0.339 ms\n\n--- google.com ping statistics ---\n1 packets transmitted, 1 packets received, 0.0% packet loss\nround-trip min/avg/max/stddev = 0.339/0.339/0.339/nan ms\n', stderr=b'')
