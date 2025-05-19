from datetime import datetime
from fastapi import APIRouter, Depends, Request
from pydantic_validation_decorator import ValidateFields
from sqlalchemy.ext.asyncio import AsyncSession
from config.enums import BusinessType
from config.get_db import get_db
from module_admin.annotation.log_annotation import Log
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.entity.vo.company_vo import CompanyModel, CompanyPageQueryModel, DeleteCompanyModel
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_admin.service.company_service import CompanyService
from module_admin.service.login_service import LoginService
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil
from config.constant import CommonConstant


companyController = APIRouter(prefix='/system/company', dependencies=[Depends(LoginService.get_current_user)])


@companyController.get(
    '/list', response_model=PageResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('system:company:list'))]
)
async def get_system_company_list(
    request: Request,
    company_page_query: CompanyPageQueryModel = Depends(CompanyPageQueryModel.as_query),
    query_db: AsyncSession = Depends(get_db),
):
    # 确保空字符串状态被视为None
    if company_page_query.status == "":
        company_page_query.status = None

    # 获取分页数据
    company_page_query_result = await CompanyService.get_company_list_services(query_db, company_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=company_page_query_result)


@companyController.post('', dependencies=[Depends(CheckUserInterfaceAuth('system:company:add'))])
@ValidateFields(validate_model='add_company')
@Log(title='公司管理', business_type=BusinessType.INSERT)
async def add_system_company(
    request: Request,
    add_company: CompanyModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    # 检查公司名称是否唯一
    unique_result = await CompanyService.check_company_name_unique_services(query_db, add_company)
    if unique_result == "1":
        return ResponseUtil.error(msg="新增公司'" + add_company.name + "'失败，公司名称已存在")

    add_company_result = await CompanyService.add_company_services(query_db, add_company)
    logger.info(add_company_result.message)

    return ResponseUtil.success(msg=add_company_result.message)


@companyController.put('', dependencies=[Depends(CheckUserInterfaceAuth('system:company:edit'))])
@ValidateFields(validate_model='edit_company')
@Log(title='公司管理', business_type=BusinessType.UPDATE)
async def edit_system_company(
    request: Request,
    edit_company: CompanyModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    # 检查公司名称是否唯一
    unique_result = await CompanyService.check_company_name_unique_services(query_db, edit_company)
    if unique_result == "1":
        return ResponseUtil.error(msg="修改公司'" + edit_company.name + "'失败，公司名称已存在")

    edit_company_result = await CompanyService.edit_company_services(query_db, edit_company)
    logger.info(edit_company_result.message)

    return ResponseUtil.success(msg=edit_company_result.message)


@companyController.delete('/{company_ids}', dependencies=[Depends(CheckUserInterfaceAuth('system:company:remove'))])
@Log(title='公司管理', business_type=BusinessType.DELETE)
async def delete_system_company(request: Request, company_ids: str, query_db: AsyncSession = Depends(get_db)):
    delete_company = DeleteCompanyModel(companyIds=company_ids)
    delete_company_result = await CompanyService.delete_company_services(query_db, delete_company)
    logger.info(delete_company_result.message)

    return ResponseUtil.success(msg=delete_company_result.message)


@companyController.get(
    '/{company_id}', response_model=CompanyModel, dependencies=[Depends(CheckUserInterfaceAuth('system:company:query'))]
)
async def get_system_company_detail(request: Request, company_id: str, query_db: AsyncSession = Depends(get_db)):
    company_detail_result = await CompanyService.company_detail_services(query_db, company_id)
    logger.info('获取成功')

    return ResponseUtil.success(data=company_detail_result)


@companyController.post(
    '/export', dependencies=[Depends(CheckUserInterfaceAuth('system:company:export'))]
)
@Log(title='公司管理', business_type=BusinessType.EXPORT)
async def export_system_company(
    request: Request,
    company_page_query: CompanyPageQueryModel = Depends(CompanyPageQueryModel.as_query),
    query_db: AsyncSession = Depends(get_db),
):
    # 确保空字符串状态被视为None
    if company_page_query.status == "":
        company_page_query.status = None

    # 导出数据
    company_export_result = await CompanyService.export_company_services(query_db, company_page_query)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(company_export_result))


