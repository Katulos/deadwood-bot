ARG VARIANT="base:bookworm"

FROM mcr.microsoft.com/devcontainers/${VARIANT}

ARG WORKSPACE=$WORKSPACE

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive && \
    apt-get -y install --no-install-recommends \
        sqlite3 \
        git-flow

# RUN wget -O $WORKSPACE/Codeium.codeium-1.48.2.vsix https://open-vsx.org/api/Codeium/codeium/1.48.2/file/Codeium.codeium-1.48.2.vsix
