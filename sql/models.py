from typing import Optional
import datetime
import decimal

from sqlalchemy import BigInteger, DECIMAL, Date, Index, Integer, String, text
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass


class StockCodeMap(Base):
    __tablename__ = 'stock_code_map'
    __table_args__ = (
        Index('idx_code', 'code'),
        Index('uk_code', 'code', unique=True),
        {'comment': '股票/指数代码与名称映射表'}
    )

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    code: Mapped[str] = mapped_column(String(20, 'utf8mb4_unicode_ci'), nullable=False, comment='股票/指数代码，如 sh.000001')
    trade_status: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text("'1'"), comment='交易状态：1=正常交易，0=停牌等')
    code_name: Mapped[str] = mapped_column(String(100, 'utf8mb4_unicode_ci'), nullable=False, comment='中文名称，如 上证综合指数')
    is_exponent: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text("'0'"), comment='是否为指数')


class StockData(Base):
    __tablename__ = 'stock_data'
    __table_args__ = (
        Index('idx_code_date', 'code', 'date'),
        Index('uk_date_code', 'date', 'code', unique=True)
    )

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    code: Mapped[str] = mapped_column(String(20, 'utf8mb4_unicode_ci'), nullable=False)
    open: Mapped[decimal.Decimal] = mapped_column(DECIMAL(16, 6), nullable=False)
    high: Mapped[decimal.Decimal] = mapped_column(DECIMAL(16, 6), nullable=False)
    low: Mapped[decimal.Decimal] = mapped_column(DECIMAL(16, 6), nullable=False)
    close: Mapped[decimal.Decimal] = mapped_column(DECIMAL(16, 6), nullable=False)
    preclose: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(16, 6))
    volume: Mapped[Optional[int]] = mapped_column(BigInteger)
    amount: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(20, 2))
    adjustflag: Mapped[Optional[int]] = mapped_column(Integer)
    turn: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(10, 6))
    tradestatus: Mapped[Optional[int]] = mapped_column(Integer)
    pctChg: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(10, 6))
    peTTM: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(16, 6))
    pbMRQ: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(16, 6))
    psTTM: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(16, 6))
    pcfNcfTTM: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(16, 6))
    isST: Mapped[Optional[int]] = mapped_column(Integer, server_default=text("'0'"))


class StockDataWeek(Base):
    __tablename__ = "stock_data_week"
    __table_args__ = (
        Index("idx_code_date", "code", "date"),
        Index("uk_date_code", "date", "code", unique=True),
    )

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    code: Mapped[str] = mapped_column(String(20, "utf8mb4_unicode_ci"), nullable=False)
    open: Mapped[decimal.Decimal] = mapped_column(DECIMAL(16, 6), nullable=False)
    high: Mapped[decimal.Decimal] = mapped_column(DECIMAL(16, 6), nullable=False)
    low: Mapped[decimal.Decimal] = mapped_column(DECIMAL(16, 6), nullable=False)
    close: Mapped[decimal.Decimal] = mapped_column(DECIMAL(16, 6), nullable=False)
    preclose: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(16, 6))
    volume: Mapped[Optional[int]] = mapped_column(BigInteger)
    amount: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(20, 2))
    adjustflag: Mapped[Optional[int]] = mapped_column(Integer)
    turn: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(10, 6))
    tradestatus: Mapped[Optional[int]] = mapped_column(Integer)
    pctChg: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(10, 6))
    peTTM: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(16, 6))
    pbMRQ: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(16, 6))
    psTTM: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(16, 6))
    pcfNcfTTM: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(16, 6))
    isST: Mapped[Optional[int]] = mapped_column(Integer, server_default=text("'0'"))


