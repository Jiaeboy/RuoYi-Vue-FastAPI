import request from '@/utils/request'

// 查询公司列表
export function listCompany(query) {
  return request({
    url: '/system/company/list',
    method: 'get',
    params: query
  })
}

// 查询公司详细
export function getCompany(id) {
  return request({
    url: '/system/company/' + id,
    method: 'get'
  })
}

// 新增公司
export function addCompany(data) {
  return request({
    url: '/system/company',
    method: 'post',
    data: data
  })
}

// 修改公司
export function updateCompany(data) {
  return request({
    url: '/system/company',
    method: 'put',
    data: data
  })
}

// 修改公司状态
export function changeCompanyStatus(id, status) {
  const data = {
    id,
    status
  }
  return request({
    url: '/system/company',
    method: 'put',
    data: data
  })
}

// 删除公司
export function delCompany(id) {
  return request({
    url: '/system/company/' + id,
    method: 'delete'
  })
}

// 导出公司已使用通用下载方法，不需要单独的API
