from setuptools import setup, find_packages

setup(
    name="tribunal-core",
    version="0.1.0",
    description="Open Core for Tribunal Multi-Agent Deliberation Engine",
    author="Tribunal Systems",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
    ],
    python_requires=">=3.8",
)
