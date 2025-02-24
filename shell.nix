{ pkgs ? import <nixpkgs> {} }:
pkgs.mkShell {
  buildInputs = [
    pkgs.python312
    pkgs.python312Packages.django
    pkgs.python312Packages.django-allauth
    pkgs.python312Packages.python-dotenv
  ];
}
