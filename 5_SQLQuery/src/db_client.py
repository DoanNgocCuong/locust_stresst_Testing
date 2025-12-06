"""
Định nghĩa client kết nối PostgreSQL để chạy câu SQL cần stress test.
Tuân thủ Single Responsibility: class này chỉ lo chuyện kết nối & execute query.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any, Tuple

import psycopg2
from psycopg2.extras import DictCursor

from config import DbConfig, QueryConfig


@dataclass
class QueryResult:
    """Đóng gói kết quả thực thi query."""

    rows: int
    duration_ms: float


class PostgresClient:
    """Client đơn giản cho PostgreSQL, mỗi Locust user giữ 1 connection riêng."""

    def __init__(self, query: str | None = None) -> None:
        self._dsn = (
            f"host={DbConfig.HOST} "
            f"port={DbConfig.PORT} "
            f"dbname={DbConfig.NAME} "
            f"user={DbConfig.USER} "
            f"password={DbConfig.PASSWORD} "
            f"connect_timeout={DbConfig.CONNECT_TIMEOUT}"
        )
        self._query = query or QueryConfig.RAW_QUERY
        self._conn = None

    def connect(self) -> None:
        """Mở connection nếu chưa có."""
        if self._conn is not None:
            return
        self._conn = psycopg2.connect(self._dsn, cursor_factory=DictCursor)

    def close(self) -> None:
        """Đóng connection."""
        if self._conn is not None:
            self._conn.close()
            self._conn = None

    def execute_query(self) -> QueryResult:
        """
        Chạy câu query mặc định và trả về số dòng + thời gian.
        """
        if self._conn is None:
            self.connect()

        assert self._conn is not None
        with self._conn.cursor() as cur:
            start = time.perf_counter()
            cur.execute(self._query)
            rows = cur.fetchall()
            end = time.perf_counter()

        duration_ms = (end - start) * 1000.0
        return QueryResult(rows=len(rows), duration_ms=duration_ms)







