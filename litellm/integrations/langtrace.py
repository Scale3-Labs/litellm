#### What this does ####
#    On success + failure, log events to Datadog

import datetime
import os
import subprocess
import sys
import traceback
import uuid

import dotenv

import litellm
from litellm._logging import print_verbose, verbose_logger


class LangtraceLogger():
    def __init__(
        self,
        langtrace_api_key=None,
        langtrace_api_host=None,
    ):
        litellm.set_verbose=True
        print_verbose(f"Langtrace Layer init........")
        # try:
        import langtrace_python_sdk
        from langtrace_python_sdk import langtrace
        from langtrace_python_sdk.constants.exporter.langtrace_exporter import (
            LANGTRACE_REMOTE_URL,
        )
        # except Exception as e:
        #     verbose_logger.error(
        #         f"\033[91mLangtrace not installed, try running 'pip install langtrace_python_sdk' to fix this error: {e}\n{traceback.format_exc()}\033[0m"
        #     )
        #     raise Exception(
        #         f"\033[91mLangtrace not installed, try running 'pip install langtrace_python_sdk' to fix this error: {e}\n{traceback.format_exc()}\033[0m"
        #     )

        verbose_logger.debug(f"Langtrace SDK init")

        self.api_key = langtrace_api_key or os.getenv("LANGTRACE_API_KEY")
        self.api_host = langtrace_api_host or os.getenv("LANGTRACE_API_HOST") or LANGTRACE_REMOTE_URL

        self.langtrace_client = langtrace.init(
            api_key=self.api_key, api_host=self.api_host, batch=False
        )

    async def _async_log_event(
        self, kwargs, response_obj, start_time, end_time, print_verbose, user_id
    ):
        self.log_event(kwargs, response_obj, start_time, end_time, print_verbose)

    def log_event(
        self, kwargs, response_obj, start_time, end_time, user_id, print_verbose
    ):
        try:
            print_verbose(
                f"Langtrace Logging - Enters logging function for model {kwargs}"
            )
            print_verbose(f"Langtrace Logging - Response: {response_obj}")
            verbose_logger.debug(f"Langtrace Logging - Response: {response_obj}")

            trace_id = kwargs.get("metadata", {}).get("trace_id", str(uuid.uuid4()))
            # make a post request to langtrace

            print(f"Langtrace Logging - Trace ID: {trace_id}")

        except Exception as e:
            verbose_logger.debug(
                f"Langtrace Layer Error - {str(e)}\n{traceback.format_exc()}"
            )
            pass
