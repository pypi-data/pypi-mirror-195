import logging
import socket
from typing import AsyncIterator, Optional, Dict, Awaitable, Union

try:
    import asyncio
    import aioredis
    from aioredis import __version__ as aioredisversion
    STATUS = f"aioredis installed, version: {aioredisversion}"
    ENABLED = True
except ImportError:
    STATUS = "aioredis not installed"
    ENABLED = False
    aioredis = None
    redisversion = 'unkonwn'


AIOREDIS_TIMEOUT = 60.0
AIOEDIS_MAXATTEMPTS = 3
REDIS_POOL_TIMEOUT = 20
REDIS_POOL_MAXCON = 100

RETRY_ON_EXCS = (aioredis.exceptions.ConnectionError,
                 aioredis.exceptions.TimeoutError,
                 aioredis.ConnectionError,
                 aioredis.TimeoutError,
                 asyncio.exceptions.CancelledError,
                 asyncio.exceptions.TimeoutError,
                 )


class AIORedisBackend:
    def __init__(self, url: str):
        self._url = url
        self._pool = None
        self._redis = None
        self.logger = logging.getLogger(f"fuglu.extensions.AIORedisBackend")

    async def _get_redis(self, timeout: Optional[float] = None, timeout_attempts: Optional[int] = None):
        timeout = timeout if timeout else AIOREDIS_TIMEOUT
        self.logger.debug(f"(R!=None:{bool(self._redis)}) Connect to redis: {self._url}")
        if self._pool is None:
            try:
                # linux only
                socket_keepalive_options = {
                    socket.TCP_KEEPIDLE: 1,
                    socket.TCP_KEEPCNT:  5,
                    socket.TCP_KEEPINTVL: 3,
                }
            except:
                socket_keepalive_options = {}
            self._pool = aioredis.BlockingConnectionPool(timeout=REDIS_POOL_TIMEOUT,
                                                         max_connections=REDIS_POOL_MAXCON,
                                                         socket_timeout=2,
                                                         socket_keepalive=True,
                                                         socket_connect_timeout=2.0,
                                                         socket_keepalive_options=socket_keepalive_options,
                                                         retry_on_timeout=True,
                                                         ).from_url(url=self._url)
        #redis_pool = RedisPooledConn(redis_conn, socket_keepalive=True, socket_timeout=socket_timeout,
                                     #pinginterval=pinginterval)
        if self._redis is None:
            self._redis = await aioredis.StrictRedis(connection_pool=self._pool)
        return self._redis

    async def get_redis(self, timeout: Optional[float] = None, timeout_attempts: Optional[int] = None):
        if not self._redis:
            timeout = timeout if timeout else AIOREDIS_TIMEOUT
            attempts = timeout_attempts if timeout_attempts else AIOEDIS_MAXATTEMPTS
            while attempts:
                attempts -= 1
                try:
                    await self._get_redis(timeout=timeout)
                except RETRY_ON_EXCS as e:
                    self._redis = None
                    if attempts:
                        self.logger.warning(f"Connection error in 'get_redis' - retry {str(e)}")
                        await asyncio.sleep(0.1)
                    else:
                        self.logger.error(f"Connection error in 'get_redis' {str(e)}")
                except Exception as e:
                    self._redis = None
                    if attempts:
                        self.logger.warning(f"Connection error in 'get_redis' - retry: {str(e)}")
                        await asyncio.sleep(0.1)
                    else:
                        self.logger.error(f"Connection error in 'get_redis': {str(e)}", exc_info=e)

        return self._redis

    async def hgetall(self, key: bytes, timeout: Optional[float] = None, timeout_attempts: Optional[int] = None) -> Optional[bytes]:
        keydata = None
        timeout = timeout if timeout else AIOREDIS_TIMEOUT
        attempts = timeout_attempts if timeout_attempts else AIOEDIS_MAXATTEMPTS
        while attempts:
            attempts -= 1
            try:
                r = await self._get_redis(timeout=timeout)
                keydata = await asyncio.wait_for(r.hgetall(key), timeout=timeout)
                attempts = 0  # no more attempts
            except RETRY_ON_EXCS as e:
                self._redis = None
                if attempts:
                    self.logger.warning(f"Connection error in 'hgetall' - retry ({type(e)}: {str(e)})")
                    await asyncio.sleep(0.1)
                else:
                    self.logger.error(f"Connection error in 'hgetall' ({type(e)}: {str(e)})")
            except Exception as e:
                self._redis = None
                if attempts:
                    self.logger.warning(f"Connection error in 'hgetall' - retry ({type(e)}: {str(e)})")
                    await asyncio.sleep(0.1)
                else:
                    self.logger.error(f"Connection error in 'hgetall': ({type(e)}: {str(e)})", exc_info=e)
        return keydata

    async def scan_iter(self, match: str = "*", count: int = 250, timeout: Optional[float] = None, timeout_attempts: Optional[int] = None) -> Optional[AsyncIterator]:
        iterator = None
        timeout = timeout if timeout else AIOREDIS_TIMEOUT
        attempts = timeout_attempts if timeout_attempts else AIOEDIS_MAXATTEMPTS
        while attempts:
            attempts -= 1
            try:
                r = await self._get_redis(timeout=timeout)
                #iterator = await asyncio.wait_for(r.scan_iter(match=match, count=count), timeout=timeout)
                iterator = r.scan_iter(match=match, count=count)
                attempts = 0  # no more attempts
            except RETRY_ON_EXCS as e:
                self._redis = None
                if attempts:
                    self.logger.warning(f"Connection error in 'scan_iter' - retry ({type(e)}) {str(e)}")
                    await asyncio.sleep(0.1)
                else:
                    self.logger.error(f"Connection error in 'scan_iter' ({type(e)}) {str(e)}")
            except Exception as e:
                self._redis = None
                if attempts:
                    self.logger.warning(f"Connection error in 'scan_iter' - retry ({type(e)}) {str(e)}")
                    await asyncio.sleep(0.1)
                else:
                    self.logger.error(f"Connection error in 'scan_iter' ({type(e)}) {str(e)}", exc_info=e)
        if iterator:
            yield iterator

    async def hset(self, key: bytes, mapping: Dict, timeout: Optional[float] = None, timeout_attempts: Optional[int] = None) -> Awaitable:
        outdata = None
        timeout = timeout if timeout else AIOREDIS_TIMEOUT
        attempts = timeout_attempts if timeout_attempts else AIOEDIS_MAXATTEMPTS
        while attempts:
            attempts -= 1
            try:
                r = await self._get_redis(timeout=timeout)
                outdata = await asyncio.wait_for(r.hset(key, mapping=mapping), timeout=timeout)
                attempts = 0  # no more attempts
            except RETRY_ON_EXCS as e:
                self._redis = None
                if attempts:
                    self.logger.warning(f"Connection error in 'hset' - retry {str(e)}")
                    await asyncio.sleep(0.1)
                else:
                    self.logger.error(f"Connection error in 'hset' {str(e)}")
            except Exception as e:
                self._redis = None
                if attempts:
                    self.logger.warning(f"Connection error in 'hset' - retry: {str(e)}")
                    await asyncio.sleep(0.1)
                else:
                    self.logger.error(f"Connection error in 'hset': {str(e)}", exc_info=e)
        return outdata

    async def hincrby(self, key: bytes, field: bytes, increment: Union[int, float] = 1, timeout: Optional[float] = None, timeout_attempts: Optional[int] = None) -> Awaitable:
        outdata = None
        timeout = timeout if timeout else AIOREDIS_TIMEOUT
        attempts = timeout_attempts if timeout_attempts else AIOEDIS_MAXATTEMPTS
        while attempts:
            attempts -= 1
            try:
                r = await self._get_redis(timeout=timeout)
                if isinstance(increment, int):
                    outdata = await asyncio.wait_for(r.hincrby(key, field, amount=increment), timeout=timeout)
                else:
                    outdata = await asyncio.wait_for(r.hincrbyfloat(key, field, amount=increment), timeout=timeout)
                attempts = 0  # no more attempts
            except RETRY_ON_EXCS as e:
                self._redis = None
                if attempts:
                    self.logger.warning(f"Connection error in 'hset' - retry {str(e)}")
                    await asyncio.sleep(0.1)
                else:
                    self.logger.error(f"Connection error in 'hset' {str(e)}")
            except Exception as e:
                self._redis = None
                if attempts:
                    self.logger.warning(f"Connection error in 'hset' - retry: {str(e)}")
                    await asyncio.sleep(0.1)
                else:
                    self.logger.error(f"Connection error in 'hset': {str(e)}", exc_info=e)
        return outdata
