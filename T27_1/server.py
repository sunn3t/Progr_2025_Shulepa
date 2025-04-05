import socket
import datetime

HOST = 'localhost'
PORT = 65432  # будь-який вільний порт


def parse_date(date_str):
    possible_formats = [
        "%d.%m.%Y",  # dd.mm.yyyy
        "%Y-%m-%d",  # yyyy-mm-dd
        "%m/%Y/%d",  # mm/yyyy/dd
    ]
    for fmt in possible_formats:
        try:
            dt = datetime.datetime.strptime(date_str, fmt)
            return dt.strftime("%d.%m.%Y")
        except ValueError:
            pass
    return None


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Сервер запущено. Очікуємо підключення на {HOST}:{PORT}...")

        conn, addr = s.accept()
        with conn:
            print(f"Підключився клієнт із адресою: {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break

                date_str = data.decode().strip()
                converted_date = parse_date(date_str)

                if converted_date is None:
                    converted_date = "Невідомий формат"

                conn.sendall((converted_date + "\n").encode())


if __name__ == "__main__":
    main()
