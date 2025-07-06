{pkgs, ...}: {
  # Used to find the project root
  projectRootFile = "flake.nix";
  settings.excludes = [
    "LICENSE"
    ".gitignore"
    "flake.lock"
  ];
  programs = {
    actionlint.enable = true;
    alejandra.enable = true;
    black.enable = true;
    yamlfmt = {
      enable = true;
      excludes = [
        ".pre-commit-config.yaml"
      ];
    };
    toml-sort.enable = true;
    shfmt.enable = true;
  };
}
