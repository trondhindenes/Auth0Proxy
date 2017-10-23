#!/usr/bin/env python

from __future__ import print_function # Only Python 2.x
import os
import subprocess
from subprocess import Popen, PIPE

def execute(cmd):
    proc = Popen([cmd], stdout=subprocess.PIPE, shell=True)
    for line in iter(proc.stdout.readline, ''):
        print(str(line))

config = '''
<VirtualHost *:443>
        OIDCProviderIssuer https://<<auth0domain>>
        OIDCProviderAuthorizationEndpoint https://<<auth0domain>>/authorize
        OIDCProviderTokenEndpoint https://<<auth0domain>>/oauth/token
        OIDCProviderTokenEndpointAuth client_secret_post
        OIDCProviderUserInfoEndpoint https://<<auth0domain>>/userinfo
        OIDCSessionMaxDuration 0

        OIDCClientID <<auth0clientid>>
        OIDCClientSecret <<auth0clientsecret>>

        OIDCScope "openid email profile"
        #This should point to the public endpoint of your apache proxy
        OIDCRedirectURI <<thiscontainerurl>>auth/
        OIDCCryptoPassphrase <password>
        OIDCCookiePath /

        SSLEngine on
        SSLProxyEngine on
        SSLCertificateFile <<cert_file>>
        SSLCertificateKeyFile <<cert_key>>
        ServerAdmin webmaster@localhost
        DocumentRoot /var/www/html

        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined

        #Some sites have large payloads
        LimitRequestFieldSize 32768

        #Send remote user in a header to upstream just for fun
        RequestHeader set X-Remote-User expr=%{REMOTE_USER}

        #Send remote user header to downstream just for fun(client)
        Header set X-Remote-User expr=%{REMOTE_USER}

        <Location /auth/>
            AuthType openid-connect
            Require valid-user
            LogLevel debug
        </Location>

        <Location />
            AuthType openid-connect
            Require valid-user
            LogLevel debug
            ProxyPass <<proxyto>>
            ProxyPassReverse <<proxyto>>
        </Location>
</VirtualHost>
# vim: syntax=apache ts=4 sw=4 sts=4 sr noet
'''

auth0_domain = os.environ['auth0domain']
auth0_client_id = os.environ['auth0clientid']
auth0_client_secret = os.environ['auth0clientsecret']
this_url = os.environ['thiscontainerurl']
proxy_to = os.environ['proxyto']
cert_file = os.environ.get('CERT_FILE_PATH', '/home/auth0proxy.cert')
cert_key = os.environ.get('CERT_KEY_PATH', '/home/auth0proxy.key')


config = config.replace('<<auth0domain>>', auth0_domain)
config = config.replace('<<auth0clientid>>', auth0_client_id)
config = config.replace('<<auth0clientsecret>>', auth0_client_secret)
config = config.replace('<<thiscontainerurl>>', this_url)
config = config.replace('<<proxyto>>', proxy_to)
config = config.replace('<<cert_file>>', cert_file)
config = config.replace('<<cert_key>>', cert_key)

text_file = open("/etc/apache2/sites-enabled/000-default.conf", "w")
text_file.write(config)
text_file.close()

#cmd = '/usr/sbin/apachectl -DFOREGROUND'
#execute(cmd)




