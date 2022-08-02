def userinfo(claims, user):
    claims['email'] = user.email

    return claims