#
#  Copyright (c) 2018-2021 Renesas Inc.
#  Copyright (c) 2018-2021 EPAM Systems Inc.
#
import time
from contextlib import contextmanager

import grpc
from colorama import Fore, Style

from aos_prov.communication.unit.v0.generated import api_iamanager_iamanager_pb2 as api_iam_manager, \
    api_iamanager_iamanager_pb2_grpc as api_iam_manager_grpc
from aos_prov.utils.errors import BoardError
from aos_prov.utils.unit_certificate import UnitCertificate

UNIT_DEFAULT_PORT = 8089


class UnitCommunication(object):
    def __init__(self, address: str = 'localhost:8089'):
        parts = address.split(':')
        if len(parts) == 2:
            try:
                port = int(parts[1])
                if not 1 <= port <= 65535:
                    raise BoardError("Unit port is invalid")
            except ValueError:
                raise BoardError("Unit port is invalid")
        else:
            address = address + ':' + str(UNIT_DEFAULT_PORT)
        self.__unit_address = address
        print(f"Will search unit on address: {Fore.GREEN}{self.__unit_address}{Style.RESET_ALL}")

    @contextmanager
    def unit_stub(self, catch_inactive=False, wait_for_close=False):
        try:
            with grpc.insecure_channel(self.__unit_address) as channel:
                stub = api_iam_manager_grpc.IAManagerStub(channel)
                if wait_for_close:
                    def _stop_wait(state):
                        if state is grpc.ChannelConnectivity.SHUTDOWN:
                            channel.unsubscribe(_stop_wait)
                            return
                    channel.subscribe(_stop_wait, try_to_connect=False)
                yield stub
        except grpc.RpcError as e:
            if catch_inactive and \
                    not (e.code() == grpc.StatusCode.UNAVAILABLE.value and e.details() == 'Socket closed'):
                return
            elif wait_for_close and (e.code() == grpc.StatusCode.UNKNOWN.value and e.details() == 'Stream removed'):
                return

            error_text = (f"{Fore.RED}FAILED! Error occurred: {Style.RESET_ALL}"
                          f"{Fore.RED}{e.code()}: {e.details()}{Style.RESET_ALL}")
            raise BoardError(error_text)

    def get_protocol_version(self) -> int:
        return 1

    def get_system_info(self) -> (str, str):
        with self.unit_stub() as stub:
            print('Getting System Info...')
            response = stub.GetSystemInfo(api_iam_manager.google_dot_protobuf_dot_empty__pb2.Empty())
            print('System ID: ' + response.system_id)
            print('Model name: ' + response.board_model)
            return response.system_id, response.board_model

    def clear(self, certificate_type: str) -> None:
        with self.unit_stub() as stub:
            print('Clear certificate: ' + certificate_type)
            response = stub.Clear(api_iam_manager.ClearReq(type=certificate_type))
            return response

    def set_cert_owner(self, certificate_type: str, password: str) -> None:
        with self.unit_stub() as stub:
            print('Set owner: ' + certificate_type)
            response = stub.SetOwner(api_iam_manager.SetOwnerReq(type=certificate_type, password=password))
            return response

    def get_cert_types(self) -> [str]:
        with self.unit_stub() as stub:
            print('Getting certificate types to renew')
            response = stub.GetCertTypes(api_iam_manager.google_dot_protobuf_dot_empty__pb2.Empty())
            print('Will be renewed: ' + str(response.types))
            return response.types

    def create_keys(self, cert_type: str, password: str) -> UnitCertificate:
        with self.unit_stub() as stub:
            print('Generating key type:' + cert_type)
            response = stub.CreateKey(api_iam_manager.CreateKeyReq(type=cert_type, password=password))
            uc = UnitCertificate()
            uc.cert_type = response.type
            uc.csr = response.csr
            return uc

    def apply_certificate(self, unit_cert: UnitCertificate):
        with self.unit_stub() as stub:
            stub.ApplyCert(api_iam_manager.ApplyCertReq(type=unit_cert.cert_type, cert=unit_cert.certificate))

    def set_users(self, users: [str]):
        with self.unit_stub() as stub:
            stub.SetUsers(api_iam_manager.SetUsersReq(users=users))

    def encrypt_disk(self, password: str):
        print('Starting disk encryption...')
        try:
            with self.unit_stub(wait_for_close=True) as stub:
                stub.EncryptDisk(api_iam_manager.EncryptDiskReq(password=password))
                print('Encryption process is finished.')
        except BoardError as be:
            print('Disk encryption returned error.')
            print(be)

    def finish_provisioning(self):
        with self.unit_stub(True) as stub:
            stub.FinishProvisioning(api_iam_manager.google_dot_protobuf_dot_empty__pb2.Empty())

    def wait_for_connection(self):
        try:
            print('Sleep for 5 seconds...')
            time.sleep(5)
            print('Waiting for Unit reboot...')
            grpc.channel_ready_future(grpc.insecure_channel(self.__unit_address)).result(timeout=300)
            print('Unit is online')
        except grpc.FutureTimeoutError:
            raise BoardError('Board didnt went online')
