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
        buildInputs = with pkgs; [
          arduino-cli
          gnumake
          screen
        ];

        shellHook = ''
          sudo sysctl kernel.unprivileged_userns_clone=1
          zsh
          sudo sysctl kernel.unprivileged_userns_clone=0
          exit'';
      };
  };
}
