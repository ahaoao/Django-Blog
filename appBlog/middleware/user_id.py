import uuid

USER_KEY = 'uid'
TEN_YEARS = 60 * 60 * 24 * 365 * 10


class UserIDMiddleware:
    """
    将该类配置在Django settings的MIDDLEWARE中。传递request作为参数
    请求到达该类后的逻辑：先生成uid，然后把uid赋值给request对象，最后返回response时，我们设置cookie，并且设置为httponly(只在服务端能访问)
    这样用户再次请求时，就会带上同样的uid了
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        uid = self.generate_uid(request)
        request.uid = uid
        response = self.get_response(request)
        response.set_cookie(USER_KEY, uid, max_age=TEN_YEARS, httponly=True)
        return response

    @staticmethod
    def generate_uid(request):
        try:
            uid = request.COOKIES[USER_KEY]
        except KeyError:
            uid = uuid.uuid4().hex
        return uid
