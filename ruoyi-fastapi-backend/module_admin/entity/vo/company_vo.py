from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank, Size
from typing import Literal, Optional, List
from module_admin.annotation.pydantic_annotation import as_query


class CompanyModel(BaseModel):
    """
    公司表对应pydantic模型
    """

    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    id: Optional[str] = Field(default=None, description='公司ID')
    name: Optional[str] = Field(default=None, description='公司名称')
    city: Optional[str] = Field(default=None, description='城市名称')
    address: Optional[str] = Field(default=None, description='公司地址')
    address_desc: Optional[str] = Field(default=None, description='地址描述', alias='addressDesc')
    version_type_name: Optional[str] = Field(default=None, description='版本类型名称', alias='versionTypeName')
    status: Optional[str] = Field(default=None, description='状态(0:正常,1:停用)')
    is_delete: Optional[Literal['0', '1']] = Field(default='0', description='是否删除(1:已删除,0:未删除)', alias='isDelete')
    create_time: Optional[datetime] = Field(default=None, description='创建时间', alias='createTime')
    update_time: Optional[datetime] = Field(default=None, description='更新时间', alias='updateTime')

    @NotBlank(field_name='name', message='公司名称不能为空')
    @Size(field_name='name', min_length=0, max_length=100, message='公司名称长度不能超过100个字符')
    def get_name(self):
        return self.name

    @Size(field_name='city', min_length=0, max_length=50, message='城市名称长度不能超过50个字符')
    def get_city(self):
        return self.city

    @Size(field_name='address', min_length=0, max_length=255, message='公司地址长度不能超过255个字符')
    def get_address(self):
        return self.address

    @Size(field_name='address_desc', min_length=0, max_length=255, message='地址描述长度不能超过255个字符')
    def get_address_desc(self):
        return self.address_desc

    @Size(field_name='version_type_name', min_length=0, max_length=50, message='版本类型名称长度不能超过50个字符')
    def get_version_type_name(self):
        return self.version_type_name


class CompanyQueryModel(CompanyModel):
    """
    公司管理不分页查询模型
    """

    begin_time: Optional[str] = Field(default=None, description='开始时间')
    end_time: Optional[str] = Field(default=None, description='结束时间')


@as_query
class CompanyPageQueryModel(CompanyQueryModel):
    """
    公司管理分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteCompanyModel(BaseModel):
    """
    删除公司模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    company_ids: str = Field(description='公司ID字符串，多个以逗号分隔')
