# -*- coding: UTF-8 -*-

import functools

# import pydantic
from django.conf import settings
from django.db import models as d_models
from django.http import HttpResponse, JsonResponse
from django.views import View
from rest_framework import status
from rest_framework.views import APIView

from ..models import Configure
from ..services import config_service
from ..utils.custom_response import util_response
from ..utils.custom_tool import request_params_wrapper
from ..utils.model_handle import model_select, parse_model


def result_json(func):
    def convert_model(v):
        dv = {}
        for f in v._meta.fields:
            fv = getattr(v, f.name)
            if isinstance(f, (d_models.ImageField, d_models.FileField)):
                if str(fv):
                    fv = "{}{}".format(settings.MEDIA_URL, fv)
                else:
                    fv = None
            if not isinstance(fv, d_models.Model):
                dv[f.name] = fv
        return dv

    def serializer(d):
        iter = None
        if isinstance(d, dict):
            iter = d.items()
        elif isinstance(d, list):
            iter = enumerate(d)
        if iter:
            for k, v in iter:
                if isinstance(v, dict) or isinstance(v, list):
                    d[k] = serializer(v)
                elif isinstance(v, (str, int, float, bool, type(None))):
                    pass
                elif isinstance(v, d_models.Model):
                    d[k] = convert_model(v)
                else:
                    d[k] = [convert_model(f) for f in v]
            # end if
        # end for
        # end if

        return d

    # end serializer

    @functools.wraps(func)
    def warpper(*args, **kwargs):
        result = serializer(func(*args, **kwargs))
        if isinstance(result, dict):
            return JsonResponse(result, safe=False, json_dumps_params={"ensure_ascii": False})
        elif isinstance(result, str):
            return HttpResponse(result)
        return result

    # end warpper

    return warpper


class DictionaryConfigure(APIView):
    # class GetResponse(pydantic.BaseModel):
    #     status: str
    #     data: typing.Any

    @request_params_wrapper
    def get(self, *args, request_params={}, **kwargs):
        """
        获取系统配置
        """
        # print("args:", args, "request_params:", request_params, "kwargs:", kwargs)
        group = request_params.get("group", None) or kwargs.get("group", None)
        key = request_params.get("key", None) or kwargs.get("key", None)
        # print("group:", group, "key", key)
        if group is None:
            return util_response(err=0, msg="group 不能为空")
        result = config_service.getConfig(group, key)
        return util_response(result, 0, status.HTTP_200_OK)

    # 添加或者修改
    @request_params_wrapper
    def post(self, *args, request_params={}, **kwargs):
        key = request_params.get('key', None) or kwargs.get("key", None)
        group = request_params.get('group', None) or kwargs.get("group", None)
        value = request_params.get('value', None) or kwargs.get("value", None)

        description = request_params.get('description', "")
        if key is None or group is None or value is None:
            return util_response(err=2055, msg="参数错误")
        config_service.setConfig(group, key, value, description)
        return util_response()

    # 删除
    def delete(self, request, key1=None):
        return config_service.delConfig(request)


# 配置列表
class DictionaryConfigurePage(View):
    def get(self, request, key1=None):
        return model_select(request, Configure)


# 批量分组展示
class BatchDictionaryConfigure(View):
    def get(self, request):
        groups = request.GET.get('groups', None)
        if groups is None:
            return util_response(None, 7568, status.HTTP_200_OK, '参数错误')
        groups = groups.split(",")
        res_set = parse_model(Configure.objects.filter(group__in=groups))
        return util_response(res_set, 0, status.HTTP_200_OK)
