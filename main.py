import argparse
import multiprocessing

from pot.config import Config
from pot.kubernetes.k8s import kubernetes_runner
from pot.models import ServiceType
from pot.ssh.ssh import ssh_runer

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', help='Path to the config YAML file')
    args = parser.parse_args()

    process_list = []
    for service in Config(args.config).services:
        match service.type:
            case ServiceType.SSH.value:
                process = multiprocessing.Process(target=ssh_runer, args=[service])
            case ServiceType.K8S.value:
                process = multiprocessing.Process(target=kubernetes_runner, args=[service])
            case _:
                print('invalid service type')
                continue

        process.start()
        process_list.append(process)

    try:
        for process in process_list:
            process.join()
    except KeyboardInterrupt:
        for process in process_list:
            process.terminate()
