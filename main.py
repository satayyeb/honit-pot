import argparse
import multiprocessing

from config import Config
from kubernetes.k8s import kubernetes_runner
from models import ServiceType
from ssh.ssh import ssh_runer

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', required=True, help='Path to the config YAML file')
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
