from rest_framework_simplejwt.authentication import JWTAuthentication


class JwtGraphQl:
    authenticator = JWTAuthentication()

    def resolve(self, next_function, root, info, **args):
        if root is None:
            try:
                auth_result = self.authenticator.authenticate(info.context)
                if auth_result is not None:
                    info.context.user = auth_result[0]
            except:
                pass

        return next_function(root, info, **args)