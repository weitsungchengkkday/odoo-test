# -*- coding: utf-8 -*-

import odoo
from odoo import api, http
from odoo.http import request

from odoo.addons.kk_oauth.domain.access_token_verifier import verify_access_token

from odoo.addons.bug_manage.common import extract_arguments
from odoo.exceptions import AccessDenied, AccessError, MissingError, RedirectWarning, UserError, ValidationError
from odoo.addons.web.controllers.main import serialize_exception,content_disposition

from odoo.addons.kk_restful.domain.json_request_body_format import format_request
from odoo.addons.kk_restful.domain.json_response_body_format import format_valid_response, format_invalid_response
from odoo.addons.kk_restful.domain.json_body_object import MetaObject, DataObject, StatusObject

import json
import base64
import logging

_logger = logging.getLogger(__name__)

class BugManage(http.Controller):

    @http.route('/api/v1/bugs/<ids>', type="http", auth="none", methods=["GET"], csrf=False)
    @verify_access_token
    @format_request
    def get_bugs(self, **kw):

        ids_str = kw.get("ids")
        ids_list = ids_str.split(",")
        id_tuple = tuple(ids_list)
        request.env.cr.execute(f"SELECT * FROM bm_bug WHERE ID IN {id_tuple}")
        data = request.env.cr.dictfetchall()
        print(type(data))

        tracking_id = kw.get('KK-Track-ID')
        tracking_seq = kw.get('KK-Track-SEQ')

        meta_object = MetaObject()
        data_object = DataObject(data=data)
        status_object = StatusObject(code="0000", message="success get bugs!!!")

        return format_valid_response(tracking_id=tracking_id, tracking_seq=tracking_seq, data_object=data_object, meta_object=meta_object, status_object=status_object, http_status=200)

    @http.route('/api/v1/multi_bugs/<ids>', type="http", auth="none", methods=["GET"], csrf=False)
    @verify_access_token
    @format_request
    def multi_bugs(self, **kw):
        ids_str = kw.get("ids")
        ids_list = ids_str.split(",")
        id_tuple = tuple(ids_list)

        tracking_id = kw.get('KK-Track-ID')
        tracking_seq = kw.get('KK-Track-SEQ')

        data = request.env['bm.bug'].sudo().search_read(
                domain=[("id", "in", id_tuple)], fields=None, offset=0, limit=None, order=False
            )
        meta_object = MetaObject(data_count=2, total_count=2)
        status_object = StatusObject(code="0000", message="success get bugs!!!!")
        data_object = DataObject(data=data)

        return format_valid_response(tracking_id=tracking_id, tracking_seq=tracking_seq, data_object=data_object, meta_object=meta_object, status_object=status_object, http_status=200)


    @http.route('/api/v1/<model>', type="http", auth="none", methods=["GET"], csrf=False)
    @verify_access_token
    @format_request
    def get_bug_list(self, **kw):
        model = kw.get("model")

        page = kw.get("page")
        page_size = kw.get("page_size")

        current_user_uid = kw.get("user_id")
        tracking_id = kw.get('KK-Track-ID')
        tracking_seq = kw.get('KK-Track-SEQ')

        try:
            domain, fields, offset, limit, order = extract_arguments(kw)
            data = request.env[model].with_user(current_user_uid).search_read(
                domain=domain, fields=fields, offset=offset, limit=limit, order=order
            )

            total_count = len(data)

            if data:

                if page and page_size:
                    quotient = total_count // int(page_size)
                    remainder = total_count % int(page_size)

                    from_data = (int(page) - 1) * int(page_size)

                    if quotient >= int(page):
                        data_count = int(page_size)
                        to_data = int(page) * int(page_size)

                    else:
                        data_count = remainder
                        to_data = (int(page) - 1) * int(page_size) + remainder

                    data = data[from_data: to_data]
                    data_object = DataObject(data=data)

                    if len(data) > 0:
                        meta_object = MetaObject(data_count=data_count, total_count=total_count)
                        status_object = StatusObject(code="0000", message="success get bugs!!!!")
                        return format_valid_response(tracking_id=tracking_id, tracking_seq=tracking_seq, data_object=data_object, meta_object=meta_object, status_object=status_object, http_status=200)
                    else:
                        meta_object = MetaObject()
                        status_object = StatusObject(code="9999", message="no bugs is found")
                        return format_invalid_response(tracking_id=tracking_id, tracking_seq=tracking_seq, meta_object=meta_object, status_object=status_object, http_status=404)

                else:
                    meta_object = MetaObject(data_count=total_count, total_count=total_count)
                    data_object = DataObject(data=data)
                    status_object = StatusObject(code="0000", message="success get bugs!!!")
                    return format_valid_response(tracking_id=tracking_id, tracking_seq=tracking_seq, data_object=data_object, meta_object=meta_object, status_object=status_object, http_status=200)

            else:
                meta_object = MetaObject()
                status_object = StatusObject(code="9999", message="no bugs is found")
                return format_invalid_response(tracking_id=tracking_id, tracking_seq=tracking_seq, meta_object=meta_object, status_object=status_object, http_status=404)

        except AccessError as e:
            meta_object = MetaObject()
            status_object = StatusObject(code="9999", message="do not have access right", detail=f"{repr(e)}")
            return format_invalid_response(tracking_id=tracking_id, tracking_seq=tracking_seq, meta_object=meta_object, status_object=status_object, http_status=403)

        except Exception as e:
            meta_object = MetaObject()
            status_object = StatusObject(code="9999", message="get bugs fail", detail=f"{repr(e)}")
            return format_invalid_response(tracking_id=tracking_id, tracking_seq=tracking_seq, meta_object=meta_object, status_object=status_object, http_status=400)


    @http.route('/api/v1/<model>/<id>', type="http", auth="none", methods=["GET"], csrf=False)
    @verify_access_token
    @format_request
    def get_bug(self, **kw):
        model = kw.get("model")
        _id = kw.get("id")

        current_user_uid = kw.get("user_id")
        tracking_id = kw.get('KK-Track-ID')
        tracking_seq = kw.get('KK-Track-SEQ')

        try:
            domain, fields, offset, limit, order = extract_arguments(kw)
            domain = [("id", "=", _id)]
            data = request.env[model].with_user(current_user_uid).search_read(
                domain=domain, fields=fields, offset=offset, limit=limit, order=order
            )
            data_object = DataObject(data=data)

            if data:
                meta_object = MetaObject(data_count=1, total_count=1)
                status_object = StatusObject(code="0000", message="success get bug !!!!")
                return format_valid_response(tracking_id=tracking_id, tracking_seq=tracking_seq, data_object=data_object, meta_object=meta_object, status_object=status_object, http_status=200)

            else:
                meta_object = MetaObject()
                status_object = StatusObject(code="9999", message="no bug is found")
                return format_invalid_response(tracking_id=tracking_id, tracking_seq=tracking_seq, meta_object=meta_object, status_object=status_object, http_status=404)

        except AccessError as e:
            meta_object = MetaObject()
            status_object = StatusObject(code="9999", message="do not have access right", detail=f"{repr(e)}")
            return format_invalid_response(tracking_id=tracking_id, tracking_seq=tracking_seq, meta_object=meta_object, status_object=status_object, http_status=403)

        except Exception as e:
            meta_object = MetaObject()
            status_object = StatusObject(code="9999", message="get bug fail", detail=f"{repr(e)}")
            return format_invalid_response(tracking_id=tracking_id, tracking_seq=tracking_seq, meta_object=meta_object, status_object=status_object, http_status=400)


    @http.route('/api/v1/<model>', type="http", auth="none", methods=["POST"], csrf=False)
    @verify_access_token
    @format_request
    def create_bug(self, **kw):
        model = kw.get('model')

        current_user_uid = kw.get("user_id")
        tracking_id = kw.get('KK-Track-ID')
        tracking_seq = kw.get('KK-Track-SEQ')
        value = kw.get('value')

        try:
            resource = request.env[model].with_user(current_user_uid).create(value)
            data = resource.read()
            data_object = DataObject(data=data)
            meta_object = MetaObject(data_count=1, total_count=1)
            status_object = StatusObject(code="0000", message="success create bug")
            return format_valid_response(tracking_id=tracking_id, tracking_seq=tracking_seq, data_object=data_object, meta_object=meta_object, status_object=status_object, http_status=201)

        except AccessError as e:
            request.env.cr.rollback()
            meta_object = MetaObject()
            status_object = StatusObject(code="9999", message="do not have access right", detail=f"{repr(e)}")
            return format_invalid_response(tracking_id=tracking_id, tracking_seq=tracking_seq, meta_object=meta_object, status_object=status_object, http_status=403)

        except Exception as e:
            request.env.cr.rollback()
            meta_object = MetaObject()
            status_object = StatusObject(code="9999", message="create bug fail", detail=f"{repr(e)}")
            return format_invalid_response(tracking_id=tracking_id, tracking_seq=tracking_seq, meta_object=meta_object, status_object=status_object, http_status=400)


    @http.route('/api/v1/<model>/<id>', type="http", auth="none", methods=["PUT"], csrf=False)
    @verify_access_token
    @format_request
    def update_bug(self, **kw):
        model = kw.get("model")
        _id = kw.get("id")

        current_user_uid = kw.get("user_id")
        tracking_id = kw.get('KK-Track-ID')
        tracking_seq = kw.get('KK-Track-SEQ')

        value = kw.get('value')

        try:
            origin = request.env[model].with_user(current_user_uid).search([("id", "=", _id)])
            data_object = DataObject(data=value)
            if origin:
                meta_object = MetaObject(data_count=1, total_count=1)
                status_object = StatusObject(code="0000", message="update bug success")
                origin.write(value)
                return format_valid_response(tracking_id=tracking_id, tracking_seq=tracking_seq, data_object=data_object, meta_object=meta_object, status_object=status_object, http_status=200)

            else:
                meta_object = MetaObject(data_count=1, total_count=1)
                status_object = StatusObject(code="0000", message=f"bug id {_id} not found, then create a new record")
                request.env[model].with_user(current_user_uid).create(value)
                return format_valid_response(tracking_id=tracking_id, tracking_seq=tracking_seq, data_object=data_object, meta_object=meta_object, status_object=status_object, http_status=200)

        except AccessError as e:
            request.env.cr.rollback()
            meta_object = MetaObject()
            status_object = StatusObject(code="9999", message="do not have access right", detail=f"{repr(e)}")
            return format_invalid_response(tracking_id=tracking_id, tracking_seq=tracking_seq, meta_object=meta_object, status_object=status_object, http_status=403)

        except Exception as e:
            request.env.cr.rollback()
            meta_object = MetaObject()
            status_object = StatusObject(code="9999", message="updatae bug fail", detail=f"{repr(e)}")
            return format_invalid_response(tracking_id=tracking_id, tracking_seq=tracking_seq, meta_object=meta_object, status_object=status_object, http_status=400)


    @http.route('/api/v1/<model>/<id>', type="http", auth="none", methods=["PATCH"], csrf=False)
    @verify_access_token
    @format_request
    def modify_bug(self, **kw):
        model = kw.get("model")
        _id = kw.get("id")

        current_user_uid = kw.get("user_id")
        tracking_id = kw.get('KK-Track-ID')
        tracking_seq = kw.get('KK-Track-SEQ')
        value = kw.get('value')

        try:
            origin = request.env[model].with_user(current_user_uid).search([("id", "=", _id)])
            data_object = DataObject(data=value)
            if origin:
                meta_object = MetaObject(data_count=1, total_count=1)
                status_object = StatusObject(code="0000", message="modify bug success")
                origin.write(value)
                return format_valid_response(tracking_id=tracking_id, tracking_seq=tracking_seq, data_object=data_object, meta_object=meta_object, status_object=status_object, http_status=200)

            else:
                meta_object = MetaObject()
                status_object = StatusObject(code="9999", message=f"bug id {_id} not exist")
                return format_invalid_response(tracking_id=tracking_id, tracking_seq=tracking_seq, meta_object=meta_object, status_object=status_object, http_status=400)

        except AccessError as e:
            request.env.cr.rollback()
            meta_object = MetaObject()
            status_object = StatusObject(code="9999", message="do not have access right", detail=f"{repr(e)}")
            return format_invalid_response(tracking_id=tracking_id, tracking_seq=tracking_seq, meta_object=meta_object, status_object=status_object, http_status=403)

        except Exception as e:
            request.env.cr.rollback()
            meta_object = MetaObject()
            status_object = StatusObject(code="9999", message="modify bug fail", detail=f"{repr(e)}")
            return format_invalid_response(tracking_id=tracking_id, tracking_seq=tracking_seq, meta_object=meta_object, status_object=status_object, http_status=400)


    @http.route('/api/v1/<model>/<id>', type="http", auth="none", methods=["DELETE"], csrf=False)
    @verify_access_token
    @format_request
    def delete_bug(self, **kw):
        model = kw.get("model")
        _id = kw.get("id")

        current_user_uid = kw.get("user_id")
        tracking_id = kw.get('KK-Track-ID')
        tracking_seq = kw.get('KK-Track-SEQ')

        try:
            record = request.env[model].with_user(current_user_uid).search([("id", "=", _id)])

            if record:
                meta_object = MetaObject(data_count=1, total_count=1)
                status_object = StatusObject(code="0000", message="delete bug success")
                data = record.read()
                data_object = DataObject(data=data)
                record.unlink()
                return format_valid_response(tracking_id=tracking_id, tracking_seq=tracking_seq, data_object=data_object, meta_object=meta_object, status_object=status_object, http_status=200)

            else:
                meta_object = MetaObject()
                status_object = StatusObject(code="9999", message=f"bug id {_id} not found")
                return format_invalid_response(tracking_id=tracking_id, tracking_seq=tracking_seq, meta_object=meta_object, status_object=status_object, http_status=400)

        except AccessError as e:
            request.env.cr.rollback()
            meta_object = MetaObject()
            status_object = StatusObject(code="9999", message="do not have access right", detail=f"{repr(e)}")
            detail = f"{repr(e)}"
            return format_invalid_response(tracking_id=tracking_id, tracking_seq=tracking_seq, meta_object=meta_object, status_object=status_object, http_status=403)

        except Exception as e:
            request.env.cr.rollback()
            meta_object = MetaObject()
            status_object = StatusObject(code="9999", message="delete bug fail", detail=f"{repr(e)}")
            return format_invalid_response(tracking_id=tracking_id, tracking_seq=tracking_seq, meta_object=meta_object, status_object=status_object, http_status=400)

