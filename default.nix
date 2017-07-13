{ pkgs ? import <nixpkgs> {}
}:

let
  python = import ./requirements.nix { inherit pkgs; };
in python.mkDerivation {
  name = "releasewarrior";
  src = ./.;
  propagatedBuildInputs = [
    python.packages."GitPython"
    python.packages."Jinja2"
  ];
}

