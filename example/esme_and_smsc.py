"""
pip install smpp_server smpplib2 
"""

###################################
# CLIENT
###################################
import sys
import logging

import smpplib2.gsm
import smpplib2.client
import smpplib2.consts

logging.basicConfig(level='DEBUG')

SMSC_SERVER_PORT = '9988'


def received_message_handler(pdu):
    return sys.stdout.write('\nSMC has sent a deliver_sm request {} {}'.format(pdu.sequence, pdu.message_id))

def smsc_message_resp_handler(pdu):
    sequence_numb = pdu.sequence
    status = pdu.status
    command_id  = pdu.command
    return sys.stdout.write('\nSMSC is responding to an ESME request {} {}'.format(pdu.sequence, pdu.message_id))

def esme_sent_msg_handler(ssm):
    body = ssm.short_message
    command_id = ssm.command
    sequence_number = ssm.sequence
    status = ssm.status
    msisdn = ssm.destination_addr
    return sys.stdout.write('\nESME is sending to SMSC {}.. command_id:{} msisdn:{} sequence_number::{}'.format(body, command_id, msisdn, sequence_number))

client = smpplib2.client.Client('127.0.0.1', SMSC_SERVER_PORT)

client.set_message_response_handler(smsc_message_resp_handler)
client.set_message_received_handler(received_message_handler)
client.set_esme_sent_msg_handler(esme_sent_msg_handler)

client.connect()
client.bind_transceiver()

ssm = client.send_message(source_addr_ton=smpplib2.consts.SMPP_TON_INTL,
        source_addr=b'254722111111',
        dest_addr_ton=smpplib2.consts.SMPP_TON_INTL,
        destination_addr=b'254722222222',
        short_message=b'hello world.')

client.listen()
client.unbind()      
client.disconnect()


###################################
# SERVER
###################################
from smpp import smsc

smsc = smsc.SMSC(SMSC_SERVER_PORT)

###################################