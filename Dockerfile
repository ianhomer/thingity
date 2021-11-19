#
# Slim image for dotfile validation
#
FROM archlinux:latest
RUN pacman -Syu --noconfirm \
  git        \
  python     \
  python-pip \
  sudo       \
  vim
RUN groupadd us && \
    useradd -m -g us me
RUN echo "me ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/me
RUN mkdir /home/me/.dotfiles/
COPY . /home/me/thingity
WORKDIR /home/me/thingity
RUN pip install -e .
COPY test/thingity.ini /home/me/.config/thingity/thingity.ini
COPY test/things /home/me/things
RUN chown -R me:us /home/me
USER me
WORKDIR /home/me
