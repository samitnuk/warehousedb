def items_proc(request):
    PORTAL_URL = request.scheme + '://' + request.get_host()
    return {'PORTAL_URL': PORTAL_URL}
