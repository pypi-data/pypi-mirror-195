import setuptools

with open("README.md", "r") as f:
    description = f.read()

setuptools.setup(
    name="django-otlp-log-exporter",
    version="1.0.1",
    author="Mojtaba Akbari",
    author_email="mojtaba.akbari.221b@gmail.com",
    packages=["otlp_exporter"],
    description="Django log handler for export your logs to otlp servers. like signoz and etc..",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/mojtabaakbari221b/django_otlp_log_exporter",
    license='MIT',
    python_requires='>=3.7',
    install_requires=[
        'opentelemetry-sdk >= 1.16.0',
        'opentelemetry-api >= 1.16.0',
        'opentelemetry-exporter-otlp >= 1.16.0',
        'Django >= 3.2',
    ],
)