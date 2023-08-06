from setuptools import find_packages, setup

with open("README.md") as f:
    long_description = f.read()

setup(
    name="flexivit_pytorch",
    packages=find_packages(),
    version="0.0.1",
    license="MIT",
    description="FlexiViT: Vision Transformer with Flexible Patch Size",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Ben Conrad",
    author_email="benwconrad@gmail.com",
    url="https://github.com/bwconrad/flexivit",
    keywords=[
        "transformers",
        "artificial intelligence",
        "computer vision",
        "deep learning",
    ],
    install_requires=[
        "einops>=0.6.0",
        "functorch>=1.13.1",
        "numpy>=1.24.2",
        "timm>=0.8.15.dev0",
        "torch>=1.13.1",
    ],
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.8",
)
