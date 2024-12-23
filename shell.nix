{ pkgs ? import <nixpkgs> {} 
}:

pkgs.mkShell {
  name="kivy-dev";
  buildInputs = [
	pkgs.vscodium
    pkgs.pipenv
	pkgs.python311Packages.uvicorn
	pkgs.python311Packages.fastapi
	pkgs.python311Packages.sqlmodel
	pkgs.python311Packages.openpyxl
	pkgs.python311Packages.pandas
	pkgs.python311Packages.numpy
	pkgs.python311Packages.jinja2
	pkgs.python311Packages.pydantic
	pkgs.python311Packages.pydantic-core
  ];
  
  shellHook = ''
  	echo "Start dev"
  	python3 main.py
  '';
}
