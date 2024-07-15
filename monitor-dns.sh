#!/bin/bash
interface=<your_network_interface>
interval=1  # in seconds
log_file="/var/log/dns_traffic.log"

while true; do
  count=$(sudo tcpdump -i $interface -c 1024 udp port 53 2>/dev/null | wc -l)
  echo "$(date): DNS queries in the last $interval second(s): $count" | tee -a $log_file
  if [ $count -ge 1024 ]; then
    echo "$(date): Warning: DNS query rate limit exceeded!" | tee -a $log_file
  fi
  sleep $interval
done