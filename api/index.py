from file_storage.wsgi import application

def handler(request, context):
    return application(request)