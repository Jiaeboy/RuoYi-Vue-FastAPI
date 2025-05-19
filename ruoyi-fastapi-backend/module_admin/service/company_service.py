from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from exceptions.exception import ServiceException
from module_admin.dao.company_dao import CompanyDao
from module_admin.entity.vo.common_vo import CrudResponseModel
from module_admin.entity.vo.company_vo import CompanyModel, CompanyPageQueryModel, DeleteCompanyModel
from utils.excel_util import ExcelUtil
from config.constant import CommonConstant


class CompanyService:
    """
    公司管理模块服务层
    """

    @classmethod
    async def get_company_list_services(
        cls, query_db: AsyncSession, query_object: CompanyPageQueryModel, is_page: bool = False
    ):
        """
        获取公司列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 公司列表信息对象
        """
        company_list_result = await CompanyDao.get_company_list(query_db, query_object, is_page)

        return company_list_result

    @classmethod
    async def company_detail_services(cls, query_db: AsyncSession, company_id: str):
        """
        根据公司id获取公司详细信息service

        :param query_db: orm对象
        :param company_id: 公司id
        :return: 公司信息对象
        """
        company_info = await CompanyDao.get_company_detail_by_id(query_db, company_id)
        if not company_info:
            raise ServiceException(message=f'ID为{company_id}的公司不存在')

        return company_info

    @classmethod
    async def add_company_services(cls, query_db: AsyncSession, page_object: CompanyModel):
        """
        新增公司service

        :param query_db: orm对象
        :param page_object: 新增公司对象
        :return: 新增公司校验结果
        """
        try:
            await CompanyDao.add_company_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_company_services(cls, query_db: AsyncSession, page_object: CompanyModel):
        """
        编辑公司service

        :param query_db: orm对象
        :param page_object: 编辑公司对象
        :return: 编辑公司校验结果
        """
        company_info = await cls.company_detail_services(query_db, page_object.id)
        if not company_info:
            raise ServiceException(message=f'ID为{page_object.id}的公司不存在')

        try:
            # 排除不需要更新的字段
            update_dict = page_object.model_dump(exclude_unset=True, exclude={'create_time', 'update_time', 'create_by', 'update_by'})
            update_dict['id'] = company_info.id
            await CompanyDao.edit_company_dao(query_db, update_dict)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='修改成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def delete_company_services(cls, query_db: AsyncSession, delete_object: DeleteCompanyModel):
        """
        删除公司service

        :param query_db: orm对象
        :param delete_object: 删除公司对象
        :return: 删除公司校验结果
        """
        company_ids = delete_object.company_ids.split(',')
        try:
            await CompanyDao.delete_company_dao(query_db, company_ids)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='删除成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def export_company_services(cls, query_db: AsyncSession, query_object: CompanyPageQueryModel):
        """
        导出公司service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :return: 导出文件字节流
        """
        company_list_result = await CompanyDao.get_company_list(query_db, query_object, is_page=False)

        # 获取导出数据

        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'id': '公司ID',
            'name': '公司名称',
            'city': '城市名称',
            'address': '公司地址',
            'addressDesc': '地址描述',
            'versionTypeName': '版本类型名称',
            'status': '状态',
            'createTime': '创建时间',
        }

        # 处理数据，确保所有字段都存在
        processed_data = []
        for item in company_list_result:
            # 处理状态显示
            status_text = '正常' if item.get('status') == '0' else '停用'

            # 创建新的数据项，确保所有字段都存在
            processed_item = {
                'id': item.get('id', ''),
                'name': item.get('name', ''),
                'city': item.get('city', ''),
                'address': item.get('address', ''),
                'addressDesc': item.get('addressDesc', ''),
                'versionTypeName': item.get('versionTypeName', ''),
                'status': status_text,
                'createTime': item.get('createTime', ''),
            }
            processed_data.append(processed_item)

        # 处理完成，准备导出

        # 使用正确的导出方法
        binary_data = ExcelUtil.export_list2excel(processed_data, mapping_dict)

        return binary_data

    @classmethod
    async def check_company_name_unique_services(cls, query_db: AsyncSession, page_object: CompanyModel):
        """
        检查公司名称是否唯一service

        :param query_db: orm对象
        :param page_object: 公司对象
        :return: 校验结果
        """
        company_id = '' if page_object.id is None else page_object.id
        company = await CompanyDao.get_company_detail_by_name(query_db, page_object.name)
        if company and company.id != company_id:
            return CommonConstant.NOT_UNIQUE  # 不唯一
        return CommonConstant.UNIQUE  # 唯一


