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
            "DECR": self.cmd_decr
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
        
        arity = {
            "PING": 0,
            "SET": 2,
            "GET": 1,
            "ECHO": 1,
            "INCR": 1,
            "DECR": 1,
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

