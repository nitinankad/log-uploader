from .uploader import LogUploader
import socket

class TermbinUploader(LogUploader):
    def upload_logs(self, log_data):
        host = "termbin.com"
        port = 9999

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.sendall(log_data.encode("utf-8"))
            response = s.recv(1024)

        url = response.decode("utf-8").strip("\n\x00")
        return url
