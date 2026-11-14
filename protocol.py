

class RESPHandler:

    def _decode_bulk_string(self, buffer: bytes):

        # b"$5 \r\n hello \r\n"
        
        crlf_first = buffer.find(b"\r\n")
        length = int(buffer[1:crlf_first])

        if length == -1:
            return (None, 5)

        payload_start = crlf_first + 2
        payload_end = payload_start + length

        if len(buffer) < payload_end + 2:
            return (None, 0)
        
        if buffer[payload_end:payload_end+2] != b"\r\n":
            return (None, 0)
        
        payload = buffer[payload_start:payload_end]
        payload = payload.decode('utf-8')

        return (payload, payload_end+2)

    def _decode_array(self, buffer: bytes):
        crlf = buffer.find(b"\r\n")
        arr_len = int(buffer[1:crlf])

        if arr_len == -1:
            return (None, 5)
        
        items = []
        cursor = crlf + 2

        for _ in range(arr_len):
            text, bytes_consumed = self.decode(buffer[cursor:])
            if bytes_consumed == 0:
                return (None, 0)
            items.append(text)
            cursor += bytes_consumed
        return (items, cursor)
    
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

        if buffer_type == b"$":
            return self._decode_bulk_string(buffer)

        if buffer_type == b"*":
            return self._decode_array(buffer)

        if buffer_type == b"-":
            error = buffer[1:crlf_index]
            error = error.decode('utf-8')

            return (error, crlf_index + 2)
        
        return (None, 0)
    
    def encode(self, value):
        crlf = b"\r\n"
        if isinstance(value, str):
            return b"+" + value.encode('utf-8') + crlf

        if type(value) == int: # bool is sub class of int so True will be encoded as integer
            return b":" + str(value).encode('utf-8') + crlf

        if isinstance(value, bytes):
            length = len(value)
            return b"$" + str(length).encode('utf-8') + crlf + value + crlf

        if value is None:
            return b"$" + str("-1").encode("utf-8") + crlf

        if isinstance(value, list):
            response = b"*" + str(len(value)).encode('utf-8') + crlf
            for item in value:
                response += self.encode(item)
            return response 

        if isinstance(value, Exception):
            return b"-" + str(value).encode('utf-8') + crlf

handler = RESPHandler()


"""
# simple Strings
print(handler.decode(b"+OK\r\n"))
print(handler.decode(b"+HELLO\r\n"))

# integers
print(handler.decode(b":42\r\n"))
print(handler.decode(b":-100\r\n"))

# bulk Strings
print(handler.decode(b"$5\r\nhello\r\n"))
print(handler.decode(b"$-1\r\n"))
print(handler.decode(b"$5\r\nhel"))

# arrays
print(handler.decode(b"*2\r\n$3\r\nGET\r\n$3\r\nkey\r\n"))
print(handler.decode(b"*1\r\n:42\r\n"))
print(handler.decode(b"*0\r\n"))
print(handler.decode(b"*2\r\n$3\r\nGET\r\n"))

# pipelined messages
buffer = b"+OK\r\n:42\r\n"

first, consumed = handler.decode(buffer)
print(first, consumed)

second, consumed = handler.decode(buffer[consumed:])
print(second, consumed)

# error 
print(handler.decode(b"-ERR unknown command\r\n"))
print(handler.decode(b"-WRONGTYPE Operation against a key holding the wrong kind of value\r\n"))

"""

