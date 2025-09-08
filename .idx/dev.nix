{ pkgs, ... }: {
  channel = "stable-24.05";
  packages = [
    pkgs.python3
    pkgs.python3Packages.pip
  ];
  idx = {
    extensions = [ "ms-python.python" ];
    workspace = {
      onStart = {
  setup = ''
    [ ! -d .venv ] && python -m venv .venv
    source .venv/bin/activate
    pip install --upgrade pip
    pip install qrcode pillow flask-socketio flask-sqlalchemy
  '';
};

    };
    previews = {
      enable = true;
      previews = {
        web = {
          command = [ "./devserver.sh" ];
          env = { PORT = "$PORT"; };
          manager = "web";
        };
      };
    };
  };
}
