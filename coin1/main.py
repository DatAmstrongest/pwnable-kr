import socket
import time

def quick_nc(host='127.0.0.1', port=9007):
    try:
        # 1. Create the socket (AF_INET = IPv4, SOCK_STREAM = TCP)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            
            # 3. Connect to the target
            print(f"Connecting to {host} on port {port}...")
            s.connect((host, port))
            
            
            data = s.recv(4096)
            print(f"Received: {data.decode('utf-8')}")
            time.sleep(3)
            for i in range(100):
                data = s.recv(4096)
                data = data.decode('utf-8')
                number_of_coins, number_of_tries=data.strip().split(" ")
                number_of_coins = number_of_coins[2:]
                number_of_tries = number_of_tries[2:]
                print(number_of_coins+" "+number_of_tries)
                start = 0
                end = int(number_of_coins)
                for trial in range(int(number_of_tries)):
                    if start < end:
                        mid = (start + end) // 2
                        weight_data = " ".join(map(str, range(start, mid + 1)))
                        s.sendall((weight_data + "\n").encode())

                        resp = s.recv(4096).decode().strip()
                        if not resp.isdigit():
                            break

                        result = int(resp)
                        if result % 10 == 0:
                            start = mid + 1
                        else:
                            end = mid
                    else:
                        s.sendall((str(start) + "\n").encode())
                        s.recv(4096)

                s.sendall((str(start) + "\n").encode())
                ans = s.recv(4096).decode()
                print(f"Server says: {ans.strip()}")
            ans = s.recv(4096).decode()
            print(f"Server says: {ans.strip()}")

    except ConnectionRefusedError:
        print("Error: Connection refused. Is the server running?")
    except socket.timeout:
        print("Error: Connection timed out.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    quick_nc()
