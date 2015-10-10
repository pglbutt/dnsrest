import logging

from dnsrest import router
from dnsrest import server

import dns.rrset

@router.route('/')
def root(request, response):
    response.answer.append(
        dns.rrset.from_text("/.", 200, "IN", "TXT", 'version: 1')
    )

if __name__ == '__main__':
    server.run(loglevel=logging.INFO)
