# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import os
import signal

import daemon
import daemon.pidfile
import sys

from .provider_battery import BatteryProvider
from .provider_cpu import CpuProvider
from .provider_datetime import DatetimeProvider
from .provider_disk_usage import DiskUsageProvider
from .provider_docker import DockerStatusProvider
from .provider_fan_speed import FanSpeedProvider
from .provider_memory import MemoryProvider
from .provider_network_country import NetworkCountryProvider
from .provider_network_latency import NetworkLatencyProvider
from .provider_temperature import TemperatureProvider
from .provider_timestamp import TimestampProvider
from .provider_weather import WeatherProvider
from .. import APP_DEV
from ..shared import (
    get_logger,
    init_logger,
    LoggerParams,
    shutdown_threads,
    IoParams,
    init_io,
    get_stdout,
    init_config,
    shutdown_started,
)
from ..shared.config import ConfigLoaderParams
from ..shared.system import get_daemon_lockfile_path


def invoke():
    os.environ.update({"ES7S_DOMAIN": "DAEMON"})
    if APP_DEV:
        init_daemon_debug()
    else:
        init_daemon_default()


def init_daemon_default():
    logger_params = LoggerParams(quiet=True)
    try:
        pidfile = daemon.pidfile.TimeoutPIDLockFile(get_daemon_lockfile_path(), 1)
        with daemon.DaemonContext(pidfile=pidfile, detach_process=False):
            d = Daemon(logger_params, None)
            d.run()
    except Exception as e:
        logger_params = LoggerParams(quiet=False)
        logger = init_logger(logger_params)
        logger.exception(e)


def init_daemon_debug():
    logger_params = LoggerParams(verbosity=3, quiet=False)
    try:
        d = Daemon(logger_params, IoParams())
        d.run()
    except Exception as e:
        get_stdout().echo(str(e))
        get_logger().exception(e)


class Daemon:
    def __init__(self, logger_params: LoggerParams, io_params: IoParams = None):
        if io_params:
            init_io(io_params)
        init_logger(params=logger_params)
        init_config(ConfigLoaderParams())

        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)
        signal.signal(signal.SIGUSR2, self.exit_gracefully)

        self._providers = [
            BatteryProvider(),
            CpuProvider(),
            DiskUsageProvider(),
            DockerStatusProvider(),
            FanSpeedProvider(),
            MemoryProvider(),
            NetworkCountryProvider(),
            NetworkLatencyProvider(),
            DatetimeProvider(),
            TemperatureProvider(),
            TimestampProvider(),
            WeatherProvider(),
        ]

    def run(self):
        for provider in self._providers:
            provider.join()

    def exit_gracefully(self, signal_code: int, *args):
        logger = get_logger(False)

        if shutdown_started():
            if logger:
                logger.info("Forcing the termination")
            os._exit(2)  # noqa
        else:
            logger.debug("Shutting threads down")
            shutdown_threads()

        if logger:
            logger.info(f"Terminating due to {signal.Signals(signal_code).name} ({signal_code})")
        sys.exit(0)
