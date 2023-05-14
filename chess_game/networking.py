import socket
from typing import Union


class ClientConnect:
    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.host, self.port))
        self.client.setblocking(False)

    def send_move(
        self, old_pos: tuple, new_pos: tuple, promotion_choice: Union[str, None]
    ) -> None:
        promotion_choice = promotion_choice if promotion_choice else "0"
        data = f"{old_pos[0]}{old_pos[1]}{new_pos[0]}{new_pos[1]}{promotion_choice}"

        # Turn data into bytes
        data = data.encode()

        self.client.send(data)

    def receive_move(self) -> tuple:
        data = self.client.recv(1024)

        # Turn data into string
        data = data.decode()
        print(data)

        return {
            "old_position": (int(data[0]), int(data[1])),
            "new_position": (int(data[2]), int(data[3])),
            "promotion_choice": data[4] if data[4] != "0" else None,
        }

    def close(self) -> None:
        self.client.close()


class ServerConnect:
    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(1)

    def send_move(
        self, old_pos: tuple, new_pos: tuple, promotion_choice: Union[str, None]
    ) -> None:
        promotion_choice = promotion_choice if promotion_choice else "0"
        data = f"{old_pos[0]}{old_pos[1]}{new_pos[0]}{new_pos[1]}{promotion_choice}"

        # Turn data into bytes
        data = data.encode()

        self.client.send(data)

    def receive_move(self) -> tuple:
        data = self.client.recv(1024)

        # Turn data into string
        data = data.decode()
        print(data)

        return {
            "old_position": (int(data[0]), int(data[1])),
            "new_position": (int(data[2]), int(data[3])),
            "promotion_choice": data[4] if data[4] != "0" else None,
        }

    def wait_for_client(self) -> None:
        self.client, self.address = self.server.accept()
        self.client.setblocking(False)

    def close(self) -> None:
        self.client.close()
        self.server.close()
