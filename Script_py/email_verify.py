import re
import smtplib
import dns.resolver

fromAddress = 'cron@bt.com'

regex = '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,})$'

inputAddress = input('Please enter the emailAddress tp verify:')
addressToverify = str(inputAddress)

match = re.match(regex, addressToverify)
if match == None:
    print('Bad Syntax')
    raise ValueError('Bad Syntax')

splitAddress = addressToverify.split('@')
domain = str(splitAddress[1])
print('Domain:', domain)

records = dns.resolver.query(domain, 'MX')
mxRecord = records[0].exchange
mxRecord = str(mxRecord)

server = smtplib.SMTP()
server.set_debuglevel(0)

server.connect(mxRecord)
server.helo(server.local_hostname)
server.mail(fromAddress)
code, message = server.rcpt(str(addressToverify))
server.quit()

if code == 250:
    print('Success')
else:
    print('Bad')