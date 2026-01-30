# =================================
# Stage 1 — Build Soar (original)
# =================================
FROM alpine:3.23 AS builder

WORKDIR /src

# === deps exatamente como no script ===
RUN apk add --no-cache \
    python3 \
    python3-dev \
    g++ \
    swig \
    tcl-dev \
    libarchive-tools \
    openjdk8 \
    patch \
    wget \
    mesa-dev \
    mesa-gl \
    glu-dev \
    libx11-dev \
    libxrandr-dev \
    libxinerama-dev \
    libxcursor-dev \
    libxi-dev

RUN ln -s /usr/lib/libtcl8.6.so /usr/lib/tcl86t.so

# === preparar diretório ===
RUN mkdir -p /src/soar

WORKDIR /src/soar

# === baixar código ===
RUN wget -c https://github.com/SoarGroup/Soar/archive/development.zip -O - \
    | bsdtar --strip-components=1 -xvf-

# === JAVA ===
ENV JAVA_HOME=/usr/lib/jvm/java-1.8-openjdk
ENV PATH="${JAVA_HOME}/bin:${PATH}"

# === patch musl ===
COPY musl-soar.patch /src/
RUN patch -p1 -i /src/musl-soar.patch

# === BUILD ===
RUN python3 /src/soar/scons/scons.py -j8 \
    CXXFLAGS="-Wno-error=unused-but-set-variable \
              -Wno-unused-but-set-variable \
              -Wno-error=return-local-addr" \
    --tcl=/usr \
    kernel \
    cli \
    scripts \
    sml_python \
    sml_tcl \
    sml_java \
    headers \
    tclsoarlib

# === package only minimal run ===
WORKDIR /src
RUN mkdir -p /opt \
 && mv /src/soar/out /src/soar/soar \
 && tar czvf soar-alpine.tgz -C /src/soar soar

# =================================
# Stage 2 — Runtime
# =================================
FROM alpine:3.23

RUN apk add --no-cache \
    libstdc++ \
    tcl \
    readline \
    ncurses \
    openjdk8-jre-base \
    python3

ENV SOAR_HOME=/opt/soar
ENV PATH="${SOAR_HOME}/bin:${PATH}"

COPY --from=builder /src/soar-alpine.tgz /tmp/
RUN cd /opt && tar xzvf /tmp/soar-alpine.tgz

# Copy Python SML server
COPY sml_server.py /opt/soar/

WORKDIR /work
EXPOSE 12122

ENTRYPOINT ["python3", "/opt/soar/sml_server.py"]
