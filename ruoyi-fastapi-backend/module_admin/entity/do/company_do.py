from datetime import datetime
from sqlalchemy import Column, DateTime, String
from config.database import Base


class Company(Base):
    """
    公司表
    """

    __tablename__ = 'company'

    id = Column(String(64), primary_key=True, comment='公司ID')
    name = Column(String(100), nullable=False, comment='公司名称')
    city = Column(String(50), nullable=True, comment='城市名称')
    address = Column(String(255), nullable=True, comment='公司地址')
    address_desc = Column(String(255), nullable=True, comment='地址描述')
    version_type_name = Column(String(50), nullable=True, comment='版本类型名称')
    status = Column(String(2), default='0', comment='状态(0:正常,1:停用)')
    is_delete = Column(String(2), default='0', comment='是否删除(1:已删除,0:未删除)')
    create_time = Column(DateTime, default=datetime.now(), comment='创建时间')
    update_time = Column(DateTime, default=datetime.now(), onupdate=datetime.now(), comment='更新时间')
