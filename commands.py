from storage import DataStore

class CommandHandler:
    def __init__(self, store: DataStore):
        self.store = store
        self.commands = {
            "PING": self.cmd_ping,
            "ECHO": self.cmd_echo,
            "SET": self.cmd_set,
            "GET": self.cmd_get,
            "DEL": self.cmd_del,
            "EXISTS": self.cmd_exists,
            "INCR": self.cmd_incr,
            "DECR": self.cmd_decr,
            "EXPIRE": self.cmd_expire,
            "TTL": self.cmd_ttl,
            "PTTL": self.cmd_pttl
        }

    def execute(self, command_list: list[str]):
        # ["SET", "name", "gojo"]
        command = command_list[0].upper()
        method = self.commands.get(command)
        if not method:
            return Exception("Command not found")

        args = command_list[1:]
        arg_count = len(args)

        if command in ("DEL", "EXISTS") and arg_count < 1:
            return Exception("Wrong number of arguments")

        if command == "SET":
            if arg_count not in (2,4):
                return Exception("Wrong number of arguments")

            if arg_count == 4 and args[2].upper() != "EX":
                return Exception("syntax error")
        
        arity = {
            "PING": 0,
            "GET": 1,
            "ECHO": 1,
            "INCR": 1,
            "DECR": 1,
            "EXPIRE": 2,
            "TTL": 1,
            "PTTL": 1
        }

        if command in arity and arity[command] != arg_count:
            return Exception("Wrong number of arguments")
        
        return method(args)

    def cmd_ping(self, args):
        return "PONG"

    def cmd_echo(self, args):
        return args[0]

    def cmd_set(self, args):
        self.store.set(args[0], args[1])
        if len(args) == 4:
            ttl = int(args[3]) * 1000
            self.store.set_expiry(args[0], ttl)
        return "OK"

    def cmd_get(self, args):
        return self.store.get(args[0])

    def cmd_exists(self, args):
        return self.store.exists(*args)

    def cmd_del(self, args):
        return self.store.delete(*args)

    def cmd_incr(self, args):
        current = self.store.get(args[0])
        if current is None:
            current = "0"

        try:
            current = int(current)
        except ValueError:
            return Exception("value is not an integer or out of range")

        current += 1
        self.store.set(args[0], str(current))
        return current

    def cmd_decr(self, args):
        current = self.store.get(args[0])
        if current is None:
            current = "0"

        try:
            current = int(current)
        except ValueError:
            return Exception("value is not an integer or out of range")

        current -= 1
        self.store.set(args[0], str(current))
        return current

    def cmd_expire(self, args):
        return self.store.set_expiry(args[0], int(args[1]) * 1000)

    def cmd_ttl(self, args):
        ttl = self.store.get_ttl_ms(args[0])
        return ttl // 1000 if ttl >= 0 else ttl

    def cmd_pttl(self, args):
        return self.store.get_ttl_ms(args[0])