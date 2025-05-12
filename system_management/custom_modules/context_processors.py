def custom_context(request):

    role_type = request.session.get("user_type")
    fullname = request.session.get("fullname")

    custom_context_data = {
        'user_type': role_type,
        'fullname': fullname
           }
    return custom_context_data