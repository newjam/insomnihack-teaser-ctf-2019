#!/usr/bin/env python3
from client import generateEncryptedVoucher
from sys import argv

print(generateEncryptedVoucher(argv[1], argv[2], argv[3]))

