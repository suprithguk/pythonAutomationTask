FROM fedora

MAINTAINER Suprith Gangawar <suprithguk@gmail.com>

RUN yum -y install python3-pip xorg-x11-server-Xvfb https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm && \
    pip install pytest-playwright pyyaml allure-pytest pyvirtualdisplay && \
    playwright install

WORKDIR /root/playwright

ENTRYPOINT ["/bin/bash"]
