FROM ubuntu:26.04

ARG UID=1000
ARG GID=1000

ARG GITHUB_TOKEN
ENV GITHUB_TOKEN=${GITHUB_TOKEN}
RUN if [ -n "$GITHUB_TOKEN" ]; then echo "GITHUB_TOKEN is set (${#GITHUB_TOKEN} characters)"; else echo "GITHUB_TOKEN is not set"; fi

ENV DEBIAN_FRONTEND=noninteractive

ENV HOME="/home/ubuntu"
ENV PATH="/home/ubuntu/.local/share/mise/shims:/home/ubuntu/.local/bin:${PATH}"

USER root

RUN apt-get update && apt-get install -y \
    openssh-server \
    zsh \
    sudo \
    curl \
    git \
    iproute2 \
    net-tools \
    iputils-ping \
    vim byobu \
    ca-certificates \
    tzdata \
    net-tools htop btop \
    nmap netcat-openbsd socat ethtool wget tinyproxy \
    apt-file \
    libatomic1 \
    docker.io \
    rsync \
    zip unzip \
    file \
    fontconfig \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN apt-file update

RUN echo "ubuntu:ubuntu" | chpasswd \
  && adduser ubuntu sudo

# Prepare SSH
RUN mkdir -p /var/run/sshd && ssh-keygen -A

# Copy external .zshrc from project directory
COPY fs/home/ubuntu/ /home/ubuntu/

# Fix ownership
RUN chown -R ubuntu:ubuntu /home/ubuntu

##RUN yes | sudo unminimize

RUN usermod -aG systemd-network ubuntu

# Install Nerd Fonts
RUN    mkdir -p /usr/share/fonts/nerd-fonts \
    && cd /usr/share/fonts/nerd-fonts \
    && wget -P /tmp https://github.com/ryanoasis/nerd-fonts/releases/download/v3.4.0/JetBrainsMono.zip \
    && wget -P /tmp https://github.com/ryanoasis/nerd-fonts/releases/download/v3.4.0/Meslo.zip \
    && unzip -o /tmp/JetBrainsMono.zip \
    && unzip -o /tmp/Meslo.zip \
    && fc-cache -fv

USER ubuntu

WORKDIR /home/ubuntu

# Install mise: https://mise.jdx.dev/getting-started.html
RUN curl https://mise.run | sh

SHELL ["/usr/bin/zsh", "-lc"]

RUN echo "HOME: $HOME"

RUN zsh -lc 'eval "$($HOME/.local/bin/mise activate zsh)" \
    && mise install'

#RUN zsh -lc 'eval "$($HOME/.local/bin/mise activate zsh)" \
#    && mise use --global gcloud \
#    && gcloud components install -q cbt bigtable'
#    #cloud-run-proxy cloud-sql-proxy app-engine-python app-engine-python-extras  gke-gcloud-auth-plugin \

RUN echo "" 

# Install oh-my-zsh: https://ohmyz.sh/
RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

# Install AstroNvim: https://astronvim.com/
RUN zsh -lc 'eval "$($HOME/.local/bin/mise activate zsh)"' \
    && git clone --depth 1 https://github.com/AstroNvim/template ~/.config/nvim \
    && rm -rf ~/.config/nvim/.git \
    && nvim --headless "+Lazy! sync" +qa

# Install https://github.com/tmux-plugins/tpm
#RUN git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm

# Install https://github.com/catppuccin/tmux
#RUN mkdir -p ~/.config/tmux/plugins/catppuccin \
#    &&  git clone -b v2.1.3 https://github.com/catppuccin/tmux.git ~/.config/tmux/plugins/catppuccin/tmux

USER root

COPY fs/home/ubuntu/.zshrc /home/ubuntu/.zshrc
# Fix ownership
RUN chown -R ubuntu:ubuntu /home/ubuntu/.zshrc

EXPOSE 22
CMD ["/usr/sbin/sshd", "-D", "-e"]
