{
  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    devenv.url = "github:cachix/devenv";
    treefmt.url = "github:numtide/treefmt-nix";
  };

  outputs = {
    self,
    flake-utils,
    nixpkgs,
    devenv,
    treefmt,
    ...
  } @ inputs:
    flake-utils.lib.eachDefaultSystem (
      system: let
        pkgs = (import nixpkgs) {
          inherit system;
          config.allowUnfree = true;
          overlays = [
          ];
        };
        treefmtEval = treefmt.lib.evalModule pkgs ./treefmt.nix;
        myTreefmt = treefmtEval.config.build.wrapper;
      in {
        packages = {
          devenv-up = self.devShells.${system}.default.config.procfileScript;
          devenv-test = self.devShells.${system}.default.config.test;
        };
        formatter = myTreefmt;
        devShells.default = devenv.lib.mkShell {
          inherit inputs pkgs;
          modules = [
            (
              {
                pkgs,
                config,
                lib,
                ...
              }: {
                packages = with pkgs; [
                  updatecli
                  myTreefmt
                  poetry
                  gitleaks
                ];
                languages = {
                  nix.enable = true;
                  python.enable = true;
                };
                git-hooks.hooks = {
                  # Github Actions
                  actionlint.enable = true;
                  # nix
                  deadnix.enable = true;
                  deadnix.settings = {
                    noLambdaArg = true;
                    noLambdaPatternNames = true;
                  };
                  flake-checker.enable = true;
                  # shell scripts
                  shellcheck.enable = true;
                  # JSON
                  check-json.enable = true;
                  # generic
                  check-toml.enable = true;
                  ripsecrets.enable = true;
                  # fmt
                  treefmt = {
                    enable = true;
                    packageOverrides.treefmt = myTreefmt;
                  };
                };

                enterShell = ''
                  [ ! -f .env ] || export $(grep -v '^#' .env | xargs)
                  echo 👋 Welcome to village-des-benjamins Development Environment. 🚀
                  echo
                  echo If you see this message, it means your are inside the Nix shell ❄️.
                  echo
                  echo ------------------------------------------------------------------
                  echo
                  echo Commands: available
                  ${pkgs.gnused}/bin/sed -e 's| |••|g' -e 's|=| |' <<EOF | ${pkgs.util-linuxMinimal}/bin/column -t | ${pkgs.gnused}/bin/sed -e 's|^|💪 |' -e 's|••| |g'
                  ${lib.generators.toKeyValue {} (lib.mapAttrs (name: value: value.description) config.scripts)}
                  EOF
                  echo
                  echo Repository:
                  echo  - https://github.com/postula/village_des_benjamins
                  echo ------------------------------------------------------------------
                  echo
                '';
              }
            )
          ];
        };
      }
    );
}
