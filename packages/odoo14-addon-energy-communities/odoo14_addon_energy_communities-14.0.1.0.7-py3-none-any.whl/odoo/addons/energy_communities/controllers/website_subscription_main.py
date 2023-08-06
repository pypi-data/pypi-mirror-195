from odoo import http
from odoo.http import request
from odoo.tools.translate import _
from odoo.addons.cooperator_website.controllers import main as emyc_wsc
from urllib.parse import urljoin
import re


class WebsiteSubscriptionCCEE(emyc_wsc.WebsiteSubscription):
    @http.route()
    def display_become_cooperator_page(self, **kwargs):

        target_odoo_company_id = False
        if kwargs.get('odoo_company_id', False):
            try:
                target_odoo_company_id = int(kwargs.get('odoo_company_id'))
            except:
                pass

        if ('odoo_company_id' in kwargs) and (
                not target_odoo_company_id or not request.env['res.company'].sudo().search(
                [('id', '=', target_odoo_company_id)])):
            return http.Response(_("Not valid parameter value [odoo_company_id]"), status=500)

        ctx = dict(request.context)
        ctx.update({'target_odoo_company_id': target_odoo_company_id})
        request.context = ctx

        res = super(WebsiteSubscriptionCCEE,
                    self).display_become_cooperator_page(**kwargs)
        return res

    @http.route()  # noqa: C901 (method too complex)
    def share_subscription(self, **kwargs):

        target_odoo_company_id = False
        if kwargs.get('company_id', False):
            try:
                target_odoo_company_id = int(kwargs.get('company_id'))
            except:
                pass

        if ('odoo_company_id' in kwargs) and (
                not target_odoo_company_id or not request.env['res.company'].sudo().search(
                [('id', '=', target_odoo_company_id)])):
            return http.Response(_("Not valid parameter value [odoo_company_id]"), status=500)

        ctx = dict(request.context)
        ctx.update({'target_odoo_company_id': target_odoo_company_id})
        request.context = ctx

        res = super(WebsiteSubscriptionCCEE,
                    self).share_subscription(**kwargs)
        return res

    def fill_values(self, values, is_company, logged, load_from_user=False):
        target_company_id = request.context.get('target_odoo_company_id', False)

        sub_req_obj = request.env["subscription.request"]
        if target_company_id:
            company = request.env['res.company'].sudo().browse(target_company_id)
        else:
            company = request.website.company_id
        products = self.get_products_share(is_company)

        if load_from_user:
            values = self.get_values_from_user(values, is_company)
        if is_company:
            values["is_company"] = "on"
        if logged:
            values["logged"] = "on"
        values["countries"] = self.get_countries()
        values["langs"] = self.get_langs()
        values["products"] = products
        fields_desc = sub_req_obj.sudo().fields_get(["company_type", "gender"])
        values["company_types"] = fields_desc["company_type"]["selection"]
        values["genders"] = fields_desc["gender"]["selection"]
        values["company"] = company

        if not values.get("share_product_id"):
            for product in products:
                if product.default_share_product is True:
                    values["share_product_id"] = product.id
                    break
            if not values.get("share_product_id", False) and products:
                values["share_product_id"] = products[0].id
        if not values.get("country_id"):
            if company.default_country_id:
                values["country_id"] = company.default_country_id.id
            else:
                values["country_id"] = 68
        if not values.get("activities_country_id"):
            if company.default_country_id:
                values["activities_country_id"] = company.default_country_id.id
            else:
                values["activities_country_id"] = 68
        if not values.get("lang"):
            if company.default_lang_id:
                values["lang"] = company.default_lang_id.code

        values.update(
            {
                "display_data_policy": company.display_data_policy_approval,
                "data_policy_required": company.data_policy_approval_required,
                "data_policy_text": company.data_policy_approval_text,
                "display_internal_rules": company.display_internal_rules_approval,
                "internal_rules_required": company.internal_rules_approval_required,
                "internal_rules_text": company.internal_rules_approval_text,
                "display_financial_risk": company.display_financial_risk_approval,
                "financial_risk_required": company.financial_risk_approval_required,
                "financial_risk_text": company.financial_risk_approval_text,
                "display_generic_rules": company.display_generic_rules_approval,
                "generic_rules_required": company.generic_rules_approval_required,
                "generic_rules_text": company.generic_rules_approval_text,
            }
        )
        return values

    def validation(  # noqa: C901 (method too complex)
            self, kwargs, logged, values, post_file
    ):
        ret = super(WebsiteSubscriptionCCEE, self).validation(kwargs, logged, values, post_file)
        target_odoo_company_id = kwargs.get('company_id') and int(kwargs.get('company_id')) or None

        redirect = "cooperator_website.becomecooperator"
        # redirect url to fall back on become coopererator in template redirection
        if target_odoo_company_id:
            values["redirect_url"] = urljoin(
                request.httprequest.host_url,
                "/page/become_cooperator?odoo_company_id={}".format(target_odoo_company_id)
            )
        else:
            values["redirect_url"] = urljoin(
                request.httprequest.host_url, "/page/become_cooperator"
            )

        email = kwargs.get("email")
        sani_vat = re.sub(r"[^a-zA-Z0-9]", "", kwargs.get("vat", "")).lower()
        is_company = kwargs.get("is_company") == "on"

        if not logged and sani_vat:
            user_in_ce = request.env['res.users'].sudo().search(
                [("login", "=", sani_vat), ('company_id', '=', target_odoo_company_id)])
            if user_in_ce:
                values = self.fill_values(values, is_company, logged)
                values.update(kwargs)
                values["error_msg"] = _(
                    "There is an existing account for this"
                    " vat number on this community. "
                    "Please contact with the community administrators."
                )
                return request.render(redirect, values)

        if not logged and email:
            user_in_ce = request.env['res.users'].sudo().search(
                [("partner_id.email", "=", email), ('company_id', '=', target_odoo_company_id)])
            if user_in_ce:
                values = self.fill_values(values, is_company, logged)
                values.update(kwargs)
                values["error_msg"] = _(
                    "There is an existing account for this"
                    " email address on this community. "
                    "Please contact with the community administrators."
                )
                return request.render(redirect, values)
        del values["redirect_url"]
        return ret
