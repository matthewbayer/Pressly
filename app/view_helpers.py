def generate_context(request, extra=None):
    logged_in = request.user.is_authenticated
    context = {"logged_in": logged_in}
    if extra:
        context = {**context, **extra}
    return context