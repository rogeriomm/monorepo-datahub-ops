FROM ubuntu:24.04

ARG UID=1000
ARG GID=1000
ARG DOCKER_GIT

ARG GITHUB_TOKEN
ENV GITHUB_TOKEN=${GITHUB_TOKEN}

ENV DEBIAN_FRONTEND=noninteractive

ENV HOME="/home/dev"
ENV PATH="/home/dev/.local/share/mise/shims:/home/dev/.local/bin:${PATH}"

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
    && rm -rf /var/lib/apt/lists/*

RUN apt-file update

# Create a non-root user with Zsh as the login shell
RUN  groupadd -o -g "${GID}" dev \
  && useradd -o -u ${UID} -g ${GID} -d /home/dev -ms /bin/zsh dev \
  && echo "dev:dev" | chpasswd \
  && adduser dev sudo

# Prepare SSH
RUN mkdir -p /var/run/sshd && ssh-keygen -A


USER dev

WORKDIR /home/dev

# Install mise: https://mise.jdx.dev/getting-started.html
RUN curl https://mise.run | sh

SHELL ["/usr/bin/zsh", "-lc"]

RUN echo "HOME: $HOME"

RUN zsh -lc 'eval "$($HOME/.local/bin/mise activate zsh)" \
    && mise use \
           neovim \
           bat yq jq zoxide fzf \
           aws-cli aws-sam  aws \
           gcloud \
           terragrunt terraform'

RUN zsh -lc 'eval "$($HOME/.local/bin/mise activate zsh)" \
    && mise use \
           argocd k9s kubecolor kubectl \
           cloudflared \
           databricks-cli \
           gh \
           github-cli'

RUN zsh -lc 'eval "$($HOME/.local/bin/mise activate zsh)" \
    && mise use \
           go \
           gum \
           helm  \
           java \
           python poetry pipx'

RUN zsh -lc 'eval "$($HOME/.local/bin/mise activate zsh)" \
    && mise use \
           java@17'

RUN zsh -lc 'eval "$($HOME/.local/bin/mise activate zsh)" \
    && mise use gcloud \
    && gcloud components install -q cbt bigtable'
    #cloud-run-proxy cloud-sql-proxy app-engine-python app-engine-python-extras  gke-gcloud-auth-plugin \

RUN echo "" 

# Install oh-my-zsh: https://ohmyz.sh/
RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

# Install AstroNvim: https://astronvim.com/
RUN git clone --depth 1 https://github.com/AstroNvim/template ~/.config/nvim \
    && rm -rf ~/.config/nvim/.git \
    && nvim --headless "+Lazy! sync" +qa

# Install https://github.com/tmux-plugins/tpm
RUN git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm

# Install https://github.com/catppuccin/tmux
RUN mkdir -p ~/.config/tmux/plugins/catppuccin \
    &&  git clone -b v2.1.3 https://github.com/catppuccin/tmux.git ~/.config/tmux/plugins/catppuccin/tmux


# Copy external .zshrc from project directory
COPY fs/home/dev/ /home/dev/

# Fix ownership
#RUN chown dev:dev /home/dev/bin


USER root

RUN yes | sudo unminimize

# Install Starship cross-shell prompt: https://github.com/starship/starship
RUN curl -sS https://starship.rs/install.sh | sh -s -- --yes

RUN apt-get update && apt-get dist-upgrade -y && apt-get install -y \
    docker.io \
    rsync \
    zip unzip \
    file \
    fontconfig \
    && rm -rf /var/lib/apt/lists/*

RUN usermod -aG systemd-network dev

# Install Nerd Fonts
RUN    mkdir -p /usr/share/fonts/nerd-fonts \
    && cd /usr/share/fonts/nerd-fonts \
    && wget -P /tmp https://github.com/ryanoasis/nerd-fonts/releases/download/v3.4.0/JetBrainsMono.zip \
    && wget -P /tmp https://github.com/ryanoasis/nerd-fonts/releases/download/v3.4.0/Meslo.zip \
    && unzip -o /tmp/JetBrainsMono.zip \
    && unzip -o /tmp/Meslo.zip \
    && fc-cache -fv

EXPOSE 22
CMD ["/usr/sbin/sshd", "-D", "-e"]
