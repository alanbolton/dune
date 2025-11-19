import socket
import errno

MIN_LENGTH_FIELD = 6 #this is ~####~ and allows a packet length of 9999

class DuneMsg :
    def __init__(self, connection, thisGame):
        self.connection = connection
        self.socket_buffer = ''
        self.rcv_msg = ''
        self.packet_rcv_inprogress = False
        self.packet_rcv_length = 0
        self.this_game = thisGame

        self.connection.setblocking(False)

    def __str__(self):
        ret_str = 'FIXME I got nothing for this\n'
        return ret_str

    def send_msg_format(self, msg):
        new_msg = '~{}~{}'.format(int(len(msg)), msg)
        return new_msg

    def rcv_input(self):
        ret_status = 0
        if len(self.socket_buffer) < MIN_LENGTH_FIELD or True == self.packet_rcv_inprogress:
            try:
                current_read = self.connection.recv(1024).decode('utf-8')
                if current_read:
                    self.socket_buffer += current_read
                else:
                    ret_status = -2

            except socket.error:
                    ret_status = -1

        if ret_status == 0:
            if False == self.packet_rcv_inprogress and len(self.socket_buffer) >= MIN_LENGTH_FIELD:
                self.packet_rcv_inprogress = True
                before, item, self.socket_buffer = self.socket_buffer.partition('~')  # remove fist ~
                if self.socket_buffer != '':
                    before, item, self.socket_buffer = self.socket_buffer.partition('~')
                    if self.socket_buffer != '':
                        self.packet_rcv_length = int(before)  # cast before into the packet length

            if len(self.socket_buffer) < self.packet_rcv_length:
                ret_status = -3
            else:
                self.packet_rcv_inprogress = False
                self.rcv_msg = self.socket_buffer[:self.packet_rcv_length]
                self.socket_buffer = self.socket_buffer[self.packet_rcv_length:]
                self.packet_rcv_length = 0
                self.this_game.process_message(self.connection, self.rcv_msg)
        return ret_status



