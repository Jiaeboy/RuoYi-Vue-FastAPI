from datetime import datetime, time
from typing import List
from sqlalchemy import and_, delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.entity.do.company_do import Company
from module_admin.entity.vo.company_vo import CompanyModel, CompanyPageQueryModel
from utils.page_util import PageUtil
import uuid


class CompanyDao:
    """
    公司管理模块数据库操作层
    """

    @classmethod
    async def get_company_detail_by_id(cls, db: AsyncSession, company_id: str):
        """
        根据公司id获取公司详细信息

        :param db: orm对象
        :param company_id: 公司id
        :return: 公司信息对象
        """
        company_info = (
            (await db.execute(select(Company).where(Company.id == company_id, Company.is_delete == '0')))
            .scalars()
            .first()
        )

        return company_info

    @classmethod
    async def get_company_list(cls, db: AsyncSession, query_object: CompanyPageQueryModel, is_page: bool = False):
        """
        获取公司列表数据

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 公司列表数据
        """
        # 构建查询条件
        conditions = [
            Company.is_delete == '0',
            Company.name.like(f'%{query_object.name}%') if query_object.name else True,
            Company.city.like(f'%{query_object.city}%') if query_object.city else True,
        ]

        # 只有明确指定状态时才进行过滤
        if query_object.status not in [None, "", "undefined", "null"]:
            conditions.append(Company.status == query_object.status)

        # 添加时间范围条件
        if query_object.begin_time and query_object.end_time:
            try:
                conditions.append(
                    Company.create_time.between(
                        datetime.combine(datetime.strptime(query_object.begin_time, '%Y-%m-%d'), time(00, 00, 00)),
                        datetime.combine(datetime.strptime(query_object.end_time, '%Y-%m-%d'), time(23, 59, 59)),
                    )
                )
            except ValueError:
                # 如果日期格式不正确，忽略时间范围条件
                pass

        query = select(Company).where(*conditions).order_by(Company.create_time.desc())

        company_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return company_list

    @classmethod
    async def add_company_dao(cls, db: AsyncSession, company: CompanyModel):
        """
        新增公司数据库操作

        :param db: orm对象
        :param company: 公司对象
        :return:
        """
        # 生成UUID作为公司ID
        company.id = str(uuid.uuid4())
        db_company = Company(**company.model_dump())
        db.add(db_company)
        await db.flush()

        return db_company

    @classmethod
    async def edit_company_dao(cls, db: AsyncSession, company: dict):
        """
        编辑公司数据库操作

        :param db: orm对象
        :param company: 需要更新的公司字典
        :return:
        """
        await db.execute(update(Company), [company])

    @classmethod
    async def delete_company_dao(cls, db: AsyncSession, company_ids: List[str]):
        """
        删除公司数据库操作（逻辑删除）

        :param db: orm对象
        :param company_ids: 公司ID列表
        :return:
        """
        await db.execute(
            update(Company)
            .where(Company.id.in_(company_ids))
            .values(is_delete='1', update_time=datetime.now())
        )

    @classmethod
    async def get_company_detail_by_name(cls, db: AsyncSession, company_name: str):
        """
        根据公司名称获取公司详细信息

        :param db: orm对象
        :param company_name: 公司名称
        :return: 公司信息对象
        """
        company_info = (
            (await db.execute(select(Company).where(Company.name == company_name, Company.is_delete == '0')))
            .scalars()
            .first()
        )

        return company_info
