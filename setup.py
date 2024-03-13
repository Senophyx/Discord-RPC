from setuptools import setup, find_packages
import re

with open('README.md') as f:
    long_description = f.read()

version = ''
with open('discordrpc/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Version is not set')


# Not needed because there are currently no required packages in requirements.txt

# def read_requirements():
#     with open('requirements.txt', 'r') as req:
#         content = req.read()
#         requirements = content.split('\n')

#     return requirements



setup(
    name='discord-rpc',
    version=version,
    author='Senophyx',
    author_email='contact@senophyx.id',
    description='An Python wrapper for Discord RPC',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT License',
    url='https://github.com/Senophyx/discord-rpc',
    project_urls={
        "Discord": "https://discord.gg/qpT2AeYZRN",
        "Documentation" : "https://github.com/Senophyx/Discord-RPC/blob/main/DOCS.md",
        "Issue tracker": "https://github.com/Senophyx/discord-rpc/issues"
    },
    packages=find_packages(),
    include_package_data=True,
    #install_requires=read_requirements(),
    keywords=["Discord", "rpc", "discord rpc"],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Other Audience',
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python'
    ]
)
