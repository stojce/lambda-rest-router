{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
	name = "python-dev";
	buildInputs = with pkgs; [
        python310
        python310Packages.pip
        python310Packages.virtualenv
        python310Packages.black
	];

    shellHook = ''
        source .venv/bin/activate
    '';
}

