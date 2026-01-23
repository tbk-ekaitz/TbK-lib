# TbK LaTeX Compilation Environment
# Based on Ubuntu with TeX Live installation

FROM ubuntu:24.04

LABEL maintainer="TbK Project"
LABEL description="LaTeX compilation environment for TbK documentation library"

# Avoid interactive prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

# Install TeX Live and required packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    texlive-latex-base \
    texlive-latex-extra \
    texlive-fonts-recommended \
    texlive-fonts-extra \
    texlive-xetex \
    texlive-luatex \
    texlive-lang-spanish \
    texlive-lang-chinese \
    latexmk \
    make \
    && rm -rf /var/lib/apt/lists/*

# Create working directory
WORKDIR /workspace

# Set default command
CMD ["bash"]
