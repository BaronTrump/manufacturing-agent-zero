FROM agent0ai/agent-zero:latest

LABEL maintainer="BaronTrump"
LABEL description="Manufacturing Agent Zero - Localized AI for Auto Part Manufacturers"

COPY agents/ /a0/agents/
COPY tools/ /a0/tools/
COPY prompts/ /a0/prompts/
COPY knowledge/ /a0/knowledge/
COPY skills/ /a0/skills/
COPY conf/ /a0/conf/

ENV DEFAULT_LANGUAGE=en
ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8

RUN mkdir -p /a0/data/vector-store /a0/data/company-kb /a0/data/config

VOLUME ["/a0/usr", "/a0/data/vector-store", "/a0/data/company-kb", "/a0/data/config"]

EXPOSE 80

CMD ["python", "run_ui.py"]
