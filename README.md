smpplib2
==============


SMPP library for Python. Forked from [https://github.com/podshumok/python-smpplib](https://github.com/podshumok/python-smpplib).

Example:
```python
import logging
import sys

import smpplib.gsm
import smpplib.client
import smpplib.consts

# if you want to know what's happening
logging.basicConfig(level='DEBUG')

# Two parts, UCS2, SMS with UDH
parts, encoding_flag, msg_type_flag = smpplib.gsm.make_parts(u'Привет мир!\n'*10)

def received_message_handler(pdu):
    return sys.stdout.write('SMSC has sent a request {} {}\n'.format(pdu.sequence, pdu.message_id))

def smsc_message_resp_handler(pdu):
    return sys.stdout.write('SMSC has sent a response to our request {} {}\n'.format(pdu.sequence, pdu.message_id))

def esme_sent_msg_handler(ssm):
    return sys.stdout.write('we are about to send message: {} with sequence_number:{} to phone_number: {}'.format(ssm.short_message, ssm.destination_addr, ssm.sequence)

client = smpplib.client.Client('example.com', SOMEPORTNUMBER)

client.set_message_response_handler(smsc_message_resp_handler)
client.set_message_received_handler(received_message_handler)
client.set_esme_sent_msg_handler(esme_sent_msg_handler)

client.connect()
client.bind_transceiver(system_id='login', password='secret')

for part in parts:
    pdu = client.send_message(
        source_addr_ton=smpplib.consts.SMPP_TON_INTL,
        #source_addr_npi=smpplib.consts.SMPP_NPI_ISDN,
        # Make sure it is a byte string, not unicode:
        source_addr='SENDERPHONENUM',

        dest_addr_ton=smpplib.consts.SMPP_TON_INTL,
        #dest_addr_npi=smpplib.consts.SMPP_NPI_ISDN,
        # Make sure thease two params are byte strings, not unicode:
        destination_addr='PHONENUMBER',
        short_message=part,

        data_coding=encoding_flag,
        esm_class=msg_type_flag,
        registered_delivery=True,
    )
    print(pdu.sequence)
client.listen()
```
You also may want to listen in a thread:
```python
from threading import Thread
t = Thread(target=client.listen)
t.start()
```

The client supports setting a custom generator that produces sequence numbers for the PDU packages. Per default a simple in memory generator is used which in conclusion is reset on (re)instantiation of the client, e.g. by an application restart. If you want to keep the sequence number to be persisted across restarts you can implement your own storage backed generator.

Example:
```python
import smpplib.client

import mymodule

generator = mymodule.PersistentSequenceGenerator()
client = smpplib.client.Client('example.com', SOMEPORTNUMBER, sequence_generator=generator)
...
```
