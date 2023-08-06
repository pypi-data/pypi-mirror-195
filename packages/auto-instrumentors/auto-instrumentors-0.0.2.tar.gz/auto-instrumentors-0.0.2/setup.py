from setuptools import setup

setup(name='auto-instrumentors',
    version='0.0.2',
    license='MIT License',
    author='Otávio Mascarenhas',
    long_description_content_type="text/markdown",
    author_email='otaviomascarenhaspessoal@gmail.com',
    keywords='instrumentors tracers metrics',
    description=u'Tool for auto create tracers and metrics to your application',
    packages=['auto_instrumentors'],
    install_requires=['prometheus_fastapi_instrumentator', 'opentelemetry-exporter-zipkin-json', 'opentelemetry.instrumentation.wsgi','opentelemetry.instrumentation.fastapi'],)