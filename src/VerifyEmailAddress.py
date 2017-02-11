import re
import smtplib
import dns.resolver
import pandas as pd


# Address used for SMTP MAIL FROM command  
fromAddress = 'teste@gmail.com'

# Simple Regex for syntax checking
regex = '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$'

def check_email(addressToVerify):
    # Syntax check
    match = re.match(regex, addressToVerify)
    if match == None:
        print('Bad Syntax')
        raise ValueError('Bad Syntax')

    # Get domain for DNS lookup
    splitAddress = addressToVerify.split('@')
    domain = str(splitAddress[1])
    print('Domain:', domain)

    # MX record lookup
    records = dns.resolver.query(domain, 'MX')
    mxRecord = records[0].exchange
    mxRecord = str(mxRecord)


    # SMTP lib setup (use debug level for full output)
    server = smtplib.SMTP()
    server.set_debuglevel(0)

    # SMTP Conversation
    server.connect(mxRecord)
    server.helo(server.local_hostname) ### server.local_hostname(Get local server hostname)
    server.mail(fromAddress)
    code, message = server.rcpt(str(addressToVerify))
    server.quit()

    #print(code)
    #print(message)

    # Assume SMTP response 250 is success
    if code == 250:
        return 'Success'
    else:
        return 'Bad'


def save(df, fname):
    df.to_csv('res/'+ fname +'.csv', header=None, sep=',')

# Email address to verify
df = pd.read_csv('res/example.csv', encoding='utf-8', header=None)


for index, row in df.iterrows():
    resp = 'bad'
    try:
        resp = check_email(str(row[1]))
    except:
        pass
    finally:
        df.loc[index, 'result'] = resp
        save(df, 'output')

