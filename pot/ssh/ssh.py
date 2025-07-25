# To run this program, the file ``ssh_host_key`` must exist with an SSH
# private key in it to use as a server host key. An SSH host certificate
# can optionally be provided in the file ``ssh_host_key-cert.pub``.
import asyncio, asyncssh, sys
from textwrap import dedent
from typing import Optional

from pot.llm import LLMApi
from pot.models import Service

ssh_service: Service

async def handle_client(process: asyncssh.SSHServerProcess) -> None:
    api = LLMApi(ssh_service, session_base=True)
    await asyncio.sleep(2)
    process.stdout.write(dedent('''
        Linux server 6.1.0-21-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.90-1 (2024-05-03) x86_64
        
        The programs included with the Debian GNU/Linux system are free software;
        the exact distribution terms for each program are described in the
        individual files in /usr/share/doc/*/copyright.
        
        Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
        permitted by applicable law.
        root@server:~$ ''').lstrip())

    def ctrl_c_handler(foo):
        pass

    process.break_received = ctrl_c_handler

    while True:
        command = await process.stdin.read(4096)

        # Ctrl+D: EOF (exit session)
        if command == '':
            process.stdout.write('\nlogout\n')
            process.exit(0)
            break
        process.stdout.write(api.chat(command).rstrip() + ' ')


class MySSHServer(asyncssh.SSHServer):
    def connection_made(self, conn: asyncssh.SSHServerConnection) -> None:
        peername = conn.get_extra_info('peername')[0]
        print(f'SSH connection received from {peername}.')

    def connection_lost(self, exc: Optional[Exception]) -> None:
        if exc:
            print('SSH connection error: ' + str(exc), file=sys.stderr)
        else:
            print('SSH connection closed.')

    def begin_auth(self, username: str) -> bool:
        return False

    def password_auth_supported(self) -> bool:
        return True


async def start_server(port: int) -> None:
    await asyncssh.create_server(
        MySSHServer,
        '',
        port,
        server_host_keys=['pot/ssh/ssh_host_key'],
        process_factory=handle_client,
    )


def ssh_runer(service: Service):
    loop = asyncio.new_event_loop()

    try:
        print(f'start listening to port {service.port}....')
        global ssh_service
        ssh_service = service
        loop.run_until_complete(start_server(service.port))
    except (OSError, asyncssh.Error) as exc:
        sys.exit('Error starting server: ' + str(exc))

    loop.run_forever()
