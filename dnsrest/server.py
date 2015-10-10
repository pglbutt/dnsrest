import logging
import socket
import SocketServer
import struct
import threading

import dns
import dns.message
import dns.rrset

import dnsrest.router
from dnsrest.router import RoutingException

LOG = logging.getLogger(__name__)


def handle_message(message):
    LOG.info("handling question '%s'", message.question[0])
    question = message.question[0]
    path = str(question.name).rstrip('.')

    response = dns.message.make_response(message)
    try:
        handler = dnsrest.router.ROUTING_TABLE.route(path)
        handler(message, response)
    except RoutingException as e:
        LOG.warning(str(e))
        response.set_rcode(dns.rcode.SERVFAIL)
    # yeah, we're authoritative
    response.flags |= dns.flags.AA

    LOG.info("returning response %s", [str(a) for a in response.answer])
    return response


# replace ThreadingTCPServer with TCPServer to run in one thread
class ThreadedTCPServer(SocketServer.ThreadingTCPServer):
    allow_reuse_address = True
    request_queue_size = 10

    def server_bind(self):
        LOG.info("Attempting to bind to %s:%s...", *self.server_address)
        SocketServer.ThreadingTCPServer.server_bind(self)
        LOG.info("Listening on %s:%s", *self.server_address)


class TCPHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        data = self.request.recv(4096)
        LOG.debug("received data '%s'", data)
        message = dns.message.from_wire(data[2:])
        LOG.debug("parsed dns query\n%s", message)
        response = handle_message(message)
        LOG.debug("sending response\n%s", response)
        payload = response.to_wire()
        resp = struct.pack("!H", len(payload)) + payload
        self.request.sendall(resp)


def run(bind_address='127.0.0.1', bind_port=53, loglevel=None):
    """Start a threaded tcp server bound to the given address/port.

    :param loglevel: one of logging.INFO, logging.DEBUG, ...
        If None, disable logging. You can also configure logging yourself.
    """
    if loglevel is not None:
        FORMAT = '%(asctime)s %(levelname)s [%(filename)s:%(lineno)s %(module)s.%(funcName)s] %(threadName)s: %(message)s'
        logging.basicConfig(level=loglevel, format=FORMAT)
    server = ThreadedTCPServer((bind_address, bind_port), TCPHandler)
    server.serve_forever()
