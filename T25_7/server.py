import socket
import threading
import os

HOST = '0.0.0.0'
PORT = 65432

SAVE_DIR = "received_files"
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

def recv_line(sock):
    line = b""
    while True:
        char = sock.recv(1)
        if not char:
            break
        if char == b'\n':
            break
        line += char
    return line.decode('utf-8')

def receive_thread(sock):
    while True:
        header = recv_line(sock)
        if not header:
            print("З'єднання закрито.")
            break
        if header.startswith("FILE:"):
            try:
                _, rest = header.split("FILE:", 1)
                filename, filesize_str = rest.split("|", 1)
                filesize = int(filesize_str)
                filename = filename.strip()
                save_path = os.path.join(SAVE_DIR, filename)
                print(f"Отримання файлу {filename} розміром {filesize} байт...")
                with open(save_path, "wb") as f:
                    remaining = filesize
                    while remaining > 0:
                        chunk = sock.recv(min(4096, remaining))
                        if not chunk:
                            break
                        f.write(chunk)
                        remaining -= len(chunk)
                print(f"Файл {filename} збережено у каталозі {SAVE_DIR}")
            except Exception as e:
                print("Помилка при отриманні файлу:", e)
        else:
            print("Отримано невідоме повідомлення:", header)

def send_file(sock, filepath):
    if not os.path.isfile(filepath):
        print("Файл не знайдено!")
        return
    try:
        filesize = os.path.getsize(filepath)
        filename = os.path.basename(filepath)
        header = f"FILE:{filename}|{filesize}\n"
        sock.sendall(header.encode('utf-8'))
        with open(filepath, "rb") as f:
            while True:
                data = f.read(4096)
                if not data:
                    break
                sock.sendall(data)
        print(f"Файл {filename} відправлено.")
    except Exception as e:
        print("Помилка при відправці файлу:", e)

def send_thread(sock):
    while True:
        command = input("Введіть команду (send <шлях_до_файлу> / exit): ")
        if command.lower().startswith("send "):
            parts = command.split(maxsplit=1)
            if len(parts) < 2:
                print("Невірна команда.")
                continue
            filepath = parts[1].strip()
            send_file(sock, filepath)
        elif command.lower() == "exit":
            print("Закриття з'єднання.")
            sock.close()
            break
        else:
            print("Невідома команда.")

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        server_sock.bind((HOST, PORT))
        server_sock.listen(1)
        print(f"Сервер запущено. Очікування підключення на {HOST}:{PORT}...")
        conn, addr = server_sock.accept()
        print("Підключено:", addr)
        t_recv = threading.Thread(target=receive_thread, args=(conn,), daemon=True)
        t_send = threading.Thread(target=send_thread, args=(conn,), daemon=True)
        t_recv.start()
        t_send.start()
        t_recv.join()
        t_send.join()
        print("З'єднання завершено.")

if __name__ == "__main__":
    main()
