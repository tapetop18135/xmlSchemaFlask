from werkzeug.wsgi import DispatcherMiddleware
from spyne.server.wsgi import WsgiApplication

from apps import spyned, spyned2
from apps.flasked import app


# SOAP services are distinct wsgi applications, we should use dispatcher
# middleware to bring all aps together
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/soapAPI1': WsgiApplication(spyned.create_app(app)),
    '/soapAPI2': WsgiApplication(spyned2.create_app(app))
})


if __name__ == '__main__':
    app.run(host = '127.0.0.1', port= 8000)