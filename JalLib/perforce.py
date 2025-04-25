import os
import subprocess
import socket
import time

class Perforce:
    def __init__(self, server=None, user=None, workspace=None):
        self.server = server if server else os.environ.get('P4PORT', "PC-BUILD:1666") # 환경 변수 우선 사용
        self.user = user if user else os.environ.get('P4USER', "Dev") # 환경 변수 우선 사용
        self.workspace = workspace if workspace else os.environ.get('P4CLIENT')
        
        os.environ['P4USER'] = self.user
        os.environ['P4PORT'] = self.server
        if self.workspace:
            os.environ['P4CLIENT'] = self.workspace
        else:
            # P4CLIENT가 None이면 환경 변수에서 제거 시도 (선택적)
            if 'P4CLIENT' in os.environ:
                del os.environ['P4CLIENT']
        
        # 초기화 시 연결 확인
        self._initialize_connection()
        
    def _initialize_connection(self):
        """Perforce 연결을 초기화합니다."""
        try:
            # 서버 연결 확인 (info 명령은 가볍고 빠르게 실행됨)
            result = subprocess.run(['p4', 'info'], 
                                   capture_output=True, 
                                   text=True, 
                                   encoding="utf-8")
            if result.returncode != 0:
                print(f"Perforce 초기화 중 경고: {result.stderr}")
        except Exception as e:
            print(f"Perforce 초기화 실패: {e}")
        
    def _run_command(self, command_args):
        """Perforce 명령을 실행하고 결과를 반환합니다."""
        self._initialize_connection()
        
        command_array = ['p4'] + command_args
        result = subprocess.run(command_array, capture_output=True, text=True, encoding="utf-8")
                
        return result.stdout.strip()

    def get_local_hostname(self):
        # 현재 로컬 머신의 호스트 이름을 반환합니다.
        return socket.gethostname()

    def get_all_clients(self):
        # 모든 클라이언트 워크스페이스의 이름을 반환합니다.
        result = self._run_command(['clients'])
        clients = []
        
        if result is None:
            return clients
            
        for line in result.splitlines():
            if line.startswith('Client'):
                parts = line.split()
                if len(parts) >= 2:
                    clients.append(parts[1])
        return clients

    def get_local_workspaces(self):
        local_hostname = self.get_local_hostname()
        all_clients = self.get_all_clients()
        local_clients = []

        for client in all_clients:
            if client.startswith(local_hostname):
                local_clients.append(client)

        return local_clients
