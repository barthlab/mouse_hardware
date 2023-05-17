{
  inputs.nixpkgs.url = "github:NixOS/nixpkgs";
  outputs = {
    self,
    nixpkgs,
  }: {
    devShells.x86_64-linux.default = with import nixpkgs {
      system = "x86_64-linux";
    };
      mkShell {
        # TODO broken for now, can't do `sudo arduino-cli`,
        # but only after nix develop, not after
        # `nix-shell -p arduino-cli gnumake screen`
        buildInputs = with pkgs; [
          arduino-cli
          gnumake
          screen
        ];

        shellHook = ''
          zsh
          exit'';
      };
  };
}
