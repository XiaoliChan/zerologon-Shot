from impacket.ldap import ldapasn1, ldap

class LDAPQuery():
    def __init__(self, domain, dc_name):
        self.domain = domain
        self.dc_name = dc_name

    def getFirstDomainAdmins(self):
        # Create the baseDN
        domainParts = self.domain.split('.')
        baseDN = ''
        for i in domainParts:
            baseDN += 'dc=%s,' % i
        # Remove last ','
        baseDN = baseDN[:-1]

        ldapConnection = ldap.LDAPConnection('ldap://%s' % self.domain, baseDN, None)
        ldapConnection.login(self.dc_name, '', self.domain, '', '')
        searchFilter = "(&(objectClass=user)(adminCount=1)(!(userAccountControl:1.2.840.113556.1.4.803:=2)))"
        a = ldapConnection.search(searchFilter=searchFilter,
                                        attributes=['sAMAccountName', 'pwdLastSet', 'mail', 'lastLogon'],
                                        sizeLimit=0)
        sAMAccountName_All = [] 
        for item in a:
            if isinstance(item, ldapasn1.SearchResultEntry) is not True:
                continue
            for attribute in item["attributes"]:
                if str(attribute['type']) == 'sAMAccountName':
                    if attribute['vals'][0].asOctets().decode('utf-8'):
                        sAMAccountName_All.append(attribute['vals'][0].asOctets().decode('utf-8'))
        
        return sAMAccountName_All[0]