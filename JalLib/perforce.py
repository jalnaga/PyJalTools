import os
import subprocess
import socket

class Perforce:
    """
    Perforce 버전 관리 시스템과의 상호작용을 위한 클래스입니다.
    
    이 클래스는 Perforce 명령을 실행하고, 워크스페이스를 관리하며
    Perforce 서버와의 연결을 제어하는 기능을 제공합니다.
    """
    
    def __init__(self, server=None, user=None, workspace=None):
        """
        Perforce 클래스의 인스턴스를 초기화합니다.
        
        Parameters:
            server (str, optional): Perforce 서버 주소. 기본값은 환경 변수 P4PORT 또는 "PC-BUILD:1666"
            user (str, optional): Perforce 사용자 이름. 기본값은 환경 변수 P4USER 또는 "Dev"
            workspace (str, optional): Perforce 워크스페이스 이름. 기본값은 환경 변수 P4CLIENT
        """
        self.server = server if server else os.environ.get('P4PORT', "PC-BUILD:1666") # 환경 변수 우선 사용
        self.user = user if user else os.environ.get('P4USER', "Dev") # 환경 변수 우선 사용
        self.workspace = workspace if workspace else os.environ.get('P4CLIENT')
        self.workSpaceRoot = None
        
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
        """
        Perforce 서버와의 연결을 초기화합니다.
        
        서버 연결을 확인하고 워크스페이스 루트 경로를 설정합니다.
        
        Returns:
            str: Perforce 서버 정보 문자열
        
        Raises:
            Exception: Perforce 연결 초기화 실패 시 예외 처리
        """
        result = None
        try:
            # 서버 연결 확인 (info 명령은 가볍고 빠르게 실행됨)
            result = subprocess.run(['p4', 'info'], 
                                   capture_output=True, 
                                   text=True, 
                                   encoding="utf-8")
            
            workSpaceRootPathResult = subprocess.run(
                ['p4', '-F', '%clientRoot%', '-ztag', 'info'],
                capture_output=True, 
                text=True, 
                encoding="utf-8"
            ).stdout.strip()
            self.workSpaceRoot = os.path.normpath(workSpaceRootPathResult)
            print(f"workSpaceRoot: {self.workSpaceRoot}")
            
            if result.returncode != 0:
                print(f"Perforce 초기화 중 경고: {result.stderr}")
        except Exception as e:
            print(f"Perforce 초기화 실패: {e}")
        
        return result.stdout.strip()
        
    def _run_command(self, inCommands):
        """
        Perforce 명령을 실행하고 결과를 반환합니다.
        
        Parameters:
            inCommands (list): 실행할 Perforce 명령어와 인수들의 리스트
        
        Returns:
            str: 명령 실행 결과 문자열
        """
        self._initialize_connection()
        
        commands = ['p4'] + inCommands
        result = subprocess.run(commands, capture_output=True, text=True, encoding="utf-8")
                
        return result.stdout.strip()

    def get_local_hostname(self):
        """
        현재 로컬 머신의 호스트 이름을 반환합니다.
        
        Returns:
            str: 로컬 머신의 호스트 이름
        """
        # 현재 로컬 머신의 호스트 이름을 반환합니다.
        return socket.gethostname()

    def get_all_clients(self):
        """
        모든 Perforce 클라이언트 워크스페이스의 이름 목록을 반환합니다.
        
        Returns:
            list: 클라이언트 워크스페이스 이름 리스트
        """
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
        """
        현재 로컬 머신에 있는 워크스페이스 목록을 반환합니다.
        
        현재 호스트 이름으로 시작하는 모든 클라이언트를 찾습니다.
        
        Returns:
            list: 로컬 머신의 워크스페이스 이름 리스트
        """
        local_hostname = self.get_local_hostname()
        all_clients = self.get_all_clients()
        local_clients = []

        for client in all_clients:
            if client.startswith(local_hostname):
                local_clients.append(client)

        return local_clients
    
    def set_workspace(self, inWorkspace):
        """
        주어진 워크스페이스로 현재 작업 환경을 전환합니다.
        
        Parameters:
            inWorkspace (str): 전환할 워크스페이스 이름
            
        Returns:
            str: 워크스페이스 정보 문자열
            
        Raises:
            ValueError: 지정된 워크스페이스가 로컬 워크스페이스 목록에 없을 경우
        """
        # 주어진 워크스페이스로 전환합니다.
        localWorkSpaces = self.get_local_workspaces()
        if workspace not in localWorkSpaces:
            raise ValueError(f"워크스페이스 '{inWorkspace}'는 로컬 워크스페이스 목록에 없습니다.")
        self.workspace = inWorkspace
        os.environ['P4CLIENT'] = self.workspace
        
        # 클라이언트 정보 확인
        result = self._run_command(['client', '-o'])
        return result
    
    def sync(self, inWorkSpace=None, inPath=None):
        """
        Perforce 워크스페이스를 최신 버전으로 동기화합니다.
        
        Parameters:
            inWorkSpace (str, optional): 동기화할 워크스페이스 이름
            inPath (str, optional): 동기화할 특정 경로
            
        Returns:
            str: 동기화 결과 문자열
        """
        # 주어진 워크스페이스를 동기화합니다.
        if inWorkSpace:
            self.workspace = inWorkSpace
            os.environ['P4CLIENT'] = self.workspace
        
        # 동기화 명령 실행
        result = self._run_command(['sync'])
        return result
