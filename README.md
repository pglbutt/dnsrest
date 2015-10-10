dnsrest
-------

This is like flask but messages are sent over dns.

Installation
------------

1. Clone this repository
2. `cd` into the cloned directory
3. `pip install -r requirements.txt`
4. `pip install .`

Example
-------

Request routing:

    from dnsrest import router
    import dns.rrset

    @router.route('/')
    def root(request, response):
        response.answer.append(
            dns.rrset.from_text("/.", 200, "IN", "TXT", 'version: 1')
        )

Get the server running:

    import logging
    from dnsrest import server

    if __name__ == '__main__':
        # binds to 127.0.0.1:53. Pass in bind_address/bind_port to override
        server.run(loglevel=logging.INFO)


Make requests:

    $ dig @localhost / +tcp +short
    "version:" "1"

Since this starts a tcp server, we pass the `+tcp` option to dig.
