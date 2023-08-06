# coding: utf-8

from __future__ import absolute_import

# import TmsClient
from huaweicloudsdktms.v1.tms_client import TmsClient
from huaweicloudsdktms.v1.tms_async_client import TmsAsyncClient
# import models into sdk package
from huaweicloudsdktms.v1.model.create_predefine_tags_request import CreatePredefineTagsRequest
from huaweicloudsdktms.v1.model.create_predefine_tags_response import CreatePredefineTagsResponse
from huaweicloudsdktms.v1.model.create_resource_tag_request import CreateResourceTagRequest
from huaweicloudsdktms.v1.model.create_resource_tag_response import CreateResourceTagResponse
from huaweicloudsdktms.v1.model.create_tag_request import CreateTagRequest
from huaweicloudsdktms.v1.model.delete_predefine_tags_request import DeletePredefineTagsRequest
from huaweicloudsdktms.v1.model.delete_predefine_tags_response import DeletePredefineTagsResponse
from huaweicloudsdktms.v1.model.delete_resource_tag_request import DeleteResourceTagRequest
from huaweicloudsdktms.v1.model.delete_resource_tag_response import DeleteResourceTagResponse
from huaweicloudsdktms.v1.model.delete_tag_request import DeleteTagRequest
from huaweicloudsdktms.v1.model.errors import Errors
from huaweicloudsdktms.v1.model.link import Link
from huaweicloudsdktms.v1.model.list_api_versions_request import ListApiVersionsRequest
from huaweicloudsdktms.v1.model.list_api_versions_response import ListApiVersionsResponse
from huaweicloudsdktms.v1.model.list_predefine_tags_request import ListPredefineTagsRequest
from huaweicloudsdktms.v1.model.list_predefine_tags_response import ListPredefineTagsResponse
from huaweicloudsdktms.v1.model.list_providers_request import ListProvidersRequest
from huaweicloudsdktms.v1.model.list_providers_response import ListProvidersResponse
from huaweicloudsdktms.v1.model.list_resource_request import ListResourceRequest
from huaweicloudsdktms.v1.model.list_resource_response import ListResourceResponse
from huaweicloudsdktms.v1.model.list_tag_keys_request import ListTagKeysRequest
from huaweicloudsdktms.v1.model.list_tag_keys_response import ListTagKeysResponse
from huaweicloudsdktms.v1.model.list_tag_values_request import ListTagValuesRequest
from huaweicloudsdktms.v1.model.list_tag_values_response import ListTagValuesResponse
from huaweicloudsdktms.v1.model.modify_prefine_tag import ModifyPrefineTag
from huaweicloudsdktms.v1.model.page_info_tag_keys import PageInfoTagKeys
from huaweicloudsdktms.v1.model.page_info_tag_values import PageInfoTagValues
from huaweicloudsdktms.v1.model.predefine_tag import PredefineTag
from huaweicloudsdktms.v1.model.predefine_tag_request import PredefineTagRequest
from huaweicloudsdktms.v1.model.provider_response_body import ProviderResponseBody
from huaweicloudsdktms.v1.model.req_create_predefine_tag import ReqCreatePredefineTag
from huaweicloudsdktms.v1.model.req_create_tag import ReqCreateTag
from huaweicloudsdktms.v1.model.req_delete_predefine_tag import ReqDeletePredefineTag
from huaweicloudsdktms.v1.model.req_delete_tag import ReqDeleteTag
from huaweicloudsdktms.v1.model.resource_tag_body import ResourceTagBody
from huaweicloudsdktms.v1.model.resource_type_body import ResourceTypeBody
from huaweicloudsdktms.v1.model.resources import Resources
from huaweicloudsdktms.v1.model.resq_tag_resource import ResqTagResource
from huaweicloudsdktms.v1.model.show_api_version_request import ShowApiVersionRequest
from huaweicloudsdktms.v1.model.show_api_version_response import ShowApiVersionResponse
from huaweicloudsdktms.v1.model.show_resource_tag_request import ShowResourceTagRequest
from huaweicloudsdktms.v1.model.show_resource_tag_response import ShowResourceTagResponse
from huaweicloudsdktms.v1.model.show_tag_quota_request import ShowTagQuotaRequest
from huaweicloudsdktms.v1.model.show_tag_quota_response import ShowTagQuotaResponse
from huaweicloudsdktms.v1.model.tag import Tag
from huaweicloudsdktms.v1.model.tag_create_response_item import TagCreateResponseItem
from huaweicloudsdktms.v1.model.tag_delete_response_item import TagDeleteResponseItem
from huaweicloudsdktms.v1.model.tag_quota import TagQuota
from huaweicloudsdktms.v1.model.tag_vo import TagVo
from huaweicloudsdktms.v1.model.update_predefine_tags_request import UpdatePredefineTagsRequest
from huaweicloudsdktms.v1.model.update_predefine_tags_response import UpdatePredefineTagsResponse
from huaweicloudsdktms.v1.model.version_detail import VersionDetail

