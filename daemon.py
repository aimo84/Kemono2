import subprocess
import gunicorn
import sys

from src.config import Configuration

if __name__ == '__main__':
    try:
        if Configuration().development_mode:
            subprocess.Popen(
                'npm run dev',
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                shell=True,
                cwd='client'
            )
        else:
            subprocess.run(
                'npm run build',
                shell=True,
                check=True,
                cwd='client'
            )

        opts = Configuration().webserver['gunicorn_options'].items()
        opts = ' '.join(list(f'--{k} {v}' for k, v in opts))
        if not Configuration().webserver['ip_security']:
            opts += ' --forwarded_allow_ips=*'
            opts += ' --proxy_allow_ips=*'
        subprocess.run(f'''
            gunicorn \\
                { '--reload' if Configuration().development_mode else '' } \\
                --workers { Configuration().webserver['workers'] } \\
                --threads { Configuration().webserver['threads'] } \\
                {opts} \\
                -b 0.0.0.0:{ Configuration().webserver['port'] } \\
            server:app
        ''', shell=True, check=True)
    except KeyboardInterrupt:
        sys.exit()