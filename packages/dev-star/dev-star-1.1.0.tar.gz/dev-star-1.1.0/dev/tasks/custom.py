import os
from argparse import Namespace
from typing import Any, Optional

from dev.constants import ReturnCode


class CustomTask:
    def __init__(
        self, run: Optional[str], pre_step: Optional[str], post_step: Optional[str]
    ) -> None:
        self._run = run
        self._pre_step = pre_step
        self._post_step = post_step

    def _run_command(self, command: Optional[str]) -> int:
        rc = ReturnCode.OK

        if command is not None:
            try:
                rc = os.system(command)
            except KeyboardInterrupt:
                return ReturnCode.INTERRUPTED

        return rc

    def override_existing(self) -> bool:
        return self._run is not None

    def perform_pre_step(self) -> int:
        return self._run_command(self._pre_step)

    def perform_post_step(self) -> int:
        return self._run_command(self._post_step)

    def execute(self, _: Optional[Namespace], **kwargs: Any) -> int:
        rc = self.perform_pre_step()
        if rc != ReturnCode.OK:
            return rc

        rc = self._run_command(self._run)
        if rc != ReturnCode.OK:
            return rc

        return self.perform_post_step()
