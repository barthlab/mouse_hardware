{
  inputs.nixpkgs.url = "github:NixOS/nixpkgs";
  outputs = {
    self,
    nixpkgs,
  }: {
    devShells.x86_64-linux.default = with import nixpkgs {
      system = "x86_64-linux";
      config = {
        allowUnfree = true;
      };
    };
    let
      pythonPackages = python3Packages;
    in
      mkShell {
        buildInputs = with pkgs; [
          python3Full

        ];

        shellHook = ''
          ${pkgs.zsh}/bin/zsh
          exit'';
      };
  };
}

