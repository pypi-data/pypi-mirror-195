from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator, metrics
from opentelemetry import trace
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (BatchSpanProcessor,ConsoleSpanExporter)
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry import trace
from opentelemetry.exporter.zipkin.json import ZipkinExporter



class auto_monitoring_FastAPI:
    
    def __init__(self, link):
        self.link = link
    

    def add_app(self, app_):
        app = app_

        instrumentator = Instrumentator(
        should_group_status_codes=False,
        should_ignore_untemplated=True,
        should_respect_env_var=True,
        should_instrument_requests_inprogress=True,
        excluded_handlers=[".*admin.*", "/metrics"],
        env_var_name="ENABLE_METRICS",
        inprogress_name="inprogress",
        inprogress_labels=True,
        )

        instrumentator.instrument(app)

        # / metrics
        @app.on_event("startup")
        async def startup():
            Instrumentator().instrument(app).expose(app)

        resource = Resource(attributes={SERVICE_NAME: "test_api"})


        zipkin_exporter = ZipkinExporter(endpoint=self.link)
        provider = TracerProvider(resource=resource)
        processor = BatchSpanProcessor(zipkin_exporter)
        provider.add_span_processor(processor)
        trace.set_tracer_provider(provider)
        trace.set_tracer_provider(TracerProvider())
        tracer = trace.get_tracer_provider().get_tracer(__name__)
        trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))

        # Instrument the app
        FastAPIInstrumentor.instrument_app(app)






