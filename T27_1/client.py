import socket

HOST = 'localhost'
PORT = 65432


INPUT_FILE = "dates_in.txt"
OUTPUT_FILE = "dates_out.txt"


def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as fin, \
            open(OUTPUT_FILE, "w", encoding="utf-8") as fout:

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))

            for line in fin:
                line = line.strip()
                if not line:
                    continue

                s.sendall(line.encode())
                data = s.recv(1024).decode()
                fout.write(data.strip() + "\n")


if __name__ == "__main__":
    main()
