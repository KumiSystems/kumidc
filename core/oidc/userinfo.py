def userinfo(claims, user):
    claims['email'] = user.email
    claims['email_verified'] = bool(user.profile.email_verified)
    claims['given_name'] = user.profile.first_name
    claims['last_name'] = user.profile.last_name
    claims['nickname'] = user.profile.nickname
    claims['preferred_username'] = user.profile.preferred_username
    claims['website'] = user.profile.website
    claims['zoneinfo'] = user.profile.zoneinfo
    claims['phone_number'] = user.profile.phone_number
    claims['phone_number_verified'] = user.profile.phone_number_verified
    return claims