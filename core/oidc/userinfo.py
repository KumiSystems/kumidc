def userinfo(claims, user):
    claims['email'] = user.email
    claims['email_verified'] = bool(user.profile.email_verified)

    return claims