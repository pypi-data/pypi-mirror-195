##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
##

from ._version import __version__

from requests import Session
from requests.exceptions import ConnectionError
from .exceptions import NotLoggedInException, OptumiException, NoAgreementException
from .utils import dev_version, get_portal_domain_and_port, get_portal, get_portal_port

import psutil, os

sessions = {}

class CustomSession(Session):
    def __init__(self):
        super().__init__()
        self._domain_and_port = get_portal_domain_and_port()

    def get_path(self):
        return "https://" + self._domain_and_port

    def attempt_silent_login(self):
        from .login import login_rest_server
        login_status, message = login_rest_server(
            get_portal(), get_portal_port(), login_type="token", save_token=True
        )
        return login_status == 1
    
    def _make_request(self, method, url, **kwargs):
        try:
            response = super().request(method, self.get_path() + url, **kwargs)
            if (not url.endswith("/login")) and response.url.endswith("/login"):
                raise NotLoggedInException()
            if response.status_code >= 400:
                text = response.text
                if text == "User has not signed the Terms & Conditions of Service":
                    raise NoAgreementException()
                raise OptumiException(text if (text != None and len(text) > 0) else None)
            return response
        except ConnectionError as err:
            if self._domain_and_port == get_portal_domain_and_port():
                raise
        raise NotLoggedInException()

    def request(self, method, url, **kwargs):
        try:
            return self._make_request(method, url, **kwargs)
        except NotLoggedInException:
            if not ('get-redirect' in url or 'exchange-versions' in url or 'login' in url or 'logout' in url) and self.attempt_silent_login():
                return self._make_request(method, url, **kwargs)
            raise


def get_mode():
    import traceback
    for frame in reversed(traceback.extract_stack()):
        parts = frame.filename.split('/')
        if 'optumi_api' in parts:
            # print('api')
            return 'api'
        elif 'jupyterlab_optumi' in parts:
            # print('jupyterlab')
            return 'jupyterlab'
        elif parts[-1] == 'thread.py' and psutil.Process(os.getpid()).name() == 'jupyter-lab': # Jupyterlab calls optumi core functions in new threads
            # print('jupyterlab')
            return 'jupyterlab'
    return 'core'

def get_session():
    global sessions
    mode = get_mode()
    if mode in sessions:
        # if dev_version:
        #     print("Re-using session for " + mode)
        return sessions[mode]
    else:
        session = CustomSession()
        # if dev_version:
        #     print("Creating session for " + mode)
        sessions[mode] = session
        return session
