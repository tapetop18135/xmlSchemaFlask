from spyne import Iterable, Integer, Unicode, rpc, Application, ServiceBase
from spyne.protocol.http import HttpRpc
from spyne.protocol.json import JsonDocument
from spyne.protocol.soap import Soap11


class TESTService(ServiceBase):
    @rpc(Unicode, Integer, _returns=Iterable(Unicode))
    def hello(ctx, name, times):
        name = name or ctx.udc.config['HELLO']
        for i in range(times):
            yield u'Hello, %s' % name


def create_app(flask_app):
    """Creates SOAP services application and distribute Flask config into
    user con defined context for each method call.
    """
    application = Application([TESTService], 'spyne.examples.flask',
        in_protocol=Soap11(validator='lxml'),
        out_protocol=Soap11(),
    )

    # Use `method_call` hook to pass flask config to each service method
    # context. But if you have any better ideas do it, make a pull request.
    # NOTE. I refuse idea to wrap each call into Flask application context
    # because in fact we inside Spyne app context, not the Flask one.

    # def _flask_config_context(ctx):
    #     ctx.udc = UserDefinedContext(flask_app.config)
    # application.event_manager.add_listener('method_call', _flask_config_context)

    return application