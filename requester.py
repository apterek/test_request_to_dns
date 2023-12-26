# This software is released under the MIT License.
# Please see the LICENSE file for full license details.

import threading
import argparse
from scapy.all import IP, UDP, DNS, DNSQR, send
import random
from faker import Faker

REQUEST_TYPE = ["NS", "A", "MX", "TXT", "SOA", "CNAME", "AAAA"]
DNS_SERVERS = ["192.168.56.102", "192.168.56.103"]
fake = Faker()


def gen_unique_domains(count: int, thread: int) -> list:
    domain_names = set()

    while len(domain_names) < count:
        domain_name = f"{fake.domain_word()}{thread}{random.choice(['.by', '.by'])}"
        domain_names.add(domain_name)
    return list(domain_names)


def gen_unique_src_ip(count: int) -> list:
    ip_unique_set = list()
    while len(ip_unique_set) < count:
        ip_unique_set.append(str(random.randint(1, 255)) + '.' + str(random.randint(0, 255)) + '.' +
                             str(random.randint(0, 255)) + '.' + str(random.randint(0, 255)))
    return ip_unique_set


def gen_src_ports(count: int) -> list:
    return [random.randint(2000, 55535) for _ in range(count)]


def send_dns_ns_request(dns_server: str, domain: str, src_ip: str, src_port: int) -> None:
    # Craft DNS request packet
    dns_request = (
            IP(src=src_ip, dst=dns_server) /
            UDP(sport=src_port, dport=53) /
            DNS(rd=1, qd=DNSQR(qname=domain, qtype=random.choice(REQUEST_TYPE)))
    )
    send(dns_request, verbose=0)


def handler(domain_count: int, thread: int) -> None:
    # gen domain list
    gen_domain_list = gen_unique_domains(domain_count, thread)
    # gen src ip list
    src_ip = gen_unique_src_ip(domain_count)
    # gen src port list
    src_ports = gen_src_ports(domain_count)
    print(f"unique domains generated, thread: {thread}")
    dns_server_ip = random.choice(DNS_SERVERS)
    print("START SEND REQUESTS...")
    for i in range(domain_count):
        send_dns_ns_request(dns_server_ip, gen_domain_list[i], src_ip[i], src_ports[i])
    print("SEND REQUESTS ENDED")


def main(domain_count: int, count_thread: int) -> None:
    threads = []

    for i in range(count_thread):
        thread = threading.Thread(target=handler, args=(domain_count, i))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='A simple script with argparse')

    # Adding optional arguments
    parser.add_argument('-d', '--domains', type=int, help='domains count')
    parser.add_argument('-t', '--thread', type=int, help='threads count')

    # Parse the command-line arguments
    args = parser.parse_args()
    domains = args.domains
    threads_c = args.thread
    if not domains:
        domains = 1_000
    if not threads_c:
        threads_c = 10

    main(domains, threads_c)
