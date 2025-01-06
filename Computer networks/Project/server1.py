import socket
import re
class Srv:
    def __init__(s, h='127.0.0.1', p=12345):
        s.h = h
        s.p = p
        s.stds = []
        s.sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.sk.bind((s.h, s.p))
        print(f"srver started on {s.h}:{s.p}")

    def rn(s):
        while True:
            dt, adr = s.sk.recvfrom(1024)
            msg = dt.decode('utf-8')
            rsp = s.proc_msg(msg)
            s.sk.sendto(rsp.encode('utf-8'), adr)
            s.prnt_stds()

    def proc_msg(s, msg):
        pat = r'^(\d{2}-\d{4})-(CI|CO)$'
        mtch = re.match(pat, msg)
        
        if not mtch:
            return "invalid msg format. use YY-AAAA-CI or YY-AAAA-CO."
        
        std_id, act = mtch.groups()
        
        if act == 'CI':
            return s.chk_in(std_id)
        else:
            return s.chk_out(std_id)

    def chk_in(s, std_id):
        if std_id in s.stds:
            return f"presrnt"
        s.stds.append(std_id)
        return f"hello std {std_id}"

    def chk_out(s, std_id):
        if std_id not in s.stds:
            return f" Contact System Admin."
        s.stds.remove(std_id)
        return f"bye std{std_id} "

    def prnt_stds(s):
        print("Current students in the db:")
        for i, std in enumerate(s.stds, 1):
            print(f"{i}. {std}")
        print()

if __name__ == "__main__":
    srv = Srv()
    srv.rn()