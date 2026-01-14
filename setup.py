from setuptools import setup, find_packages

setup(
    name="synbio-promoter-predictor",
    version="0.1.0",
    author="Rong Fan",               # ← 改成你的真实姓名
    author_email="fandud@163.com",   # ← 改成你的邮箱（可虚构）
    description="Rule-based bacterial promoter predictor",
    packages=find_packages(),
    install_requires=["pandas"],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "promoter-predict=synbio_promoter.cli:main",
        ],
    },
)