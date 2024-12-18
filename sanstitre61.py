# -*- coding: utf-8 -*-
"""
Created on Sun Dec  8 05:12:31 2024

@author: pc
"""

import os

def load_blacklist(file):
    with open(file, "r") as f:
        return [line.strip() for line in f]

def block_blacklisted_ips(blacklist_file):
    blacklist = load_blacklist(blacklist_file)
    for ip in blacklist:
        os.system(f"sudo iptables -A INPUT -s {ip} -j DROP")
        print(f"[INFO] IP bloquée : {ip}")

# Exemple : fichier blacklist.txt contenant les IP à bloquer
block_blacklisted_ips("blacklist.txt")
