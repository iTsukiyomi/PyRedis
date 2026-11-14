

class RESPHandler:

    def decode(self, buffer: bytes):
        crlf_index = buffer.find(b'\r\n')
        if crlf_index == -1:
            return (None, 0)

        buffer_type = buffer[0:1]

        if buffer_type == b"+":
            text = buffer[1:crlf_index]
            text = text.decode('utf-8')
            return (text, crlf_index + 2)

        if buffer_type == b":":
            num = int(buffer[1:crlf_index])
            return (num, crlf_index + 2)

    def encode(self, value):
        pass

handler = RESPHandler()
print(handler.decode(b":-100\r\n"))
