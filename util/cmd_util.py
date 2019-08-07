import subprocess


def exec_cmd(cmd, timeout=10):
    code = -100
    p = None
    try:
        with subprocess.Popen(['sh', '-c', cmd], shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as p:
            code = p.wait(timeout)
            if code != 0:
                return p.stdout.read().decode('utf-8'), code
            result = p.stdout.read()
        return result.decode('utf-8'), code
    except Exception:
        return '', code
    finally:
        if p:
            p.send_signal(9)
