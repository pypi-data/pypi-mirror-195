import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="l0n0lvedio2image",
    version="1.0.2",
    author="l0n0l",
    author_email="1038352856@qq.com",
    description="视频与png图片之间的转换",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/l00n00l/l0n0lvedio2image.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires='>=3.9',
    include_package_data=True,
    install_requires=[
        "opencv-python"
    ],
    entry_points={
        "console_scripts": [
            "l0n0limg2vedio = l0n0lvedio2image.img_to_vedio:run",
            "l0n0lvedio2img = l0n0lvedio2image.vedio_to_img:run",
        ]
    }
)
