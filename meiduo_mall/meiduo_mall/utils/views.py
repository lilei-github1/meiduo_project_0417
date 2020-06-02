from django.contrib.auth.mixins import LoginRequiredMixin
from django import http


class LoginRequiredJSONMixin(LoginRequiredMixin):
    def handle_no_permission(self):
        return http.JsonResponse({'code':400,'errmsg':'用户未登录'})