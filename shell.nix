{ pkgs ? import <nixpkgs> {} }:
pkgs.mkShell {
  buildInputs = [
    pkgs.python313
    pkgs.python313Packages.django
  ];
}
