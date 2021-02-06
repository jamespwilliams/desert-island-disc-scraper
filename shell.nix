let
  pkgs = import <nixpkgs> {};
in pkgs.mkShell {
  buildInputs = [
    pkgs.python3
  ];
  shellHook = ''
    . .venv/bin/activate
    pip install -r requirements.txt | grep -v "already satisfied"
  '';
}
