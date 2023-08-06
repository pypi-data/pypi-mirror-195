from setuptools import setup
setup(

	name="RenePython",
	version="0.9",
	description="genial",
	author="René Lázaro Collado Arteaga",
	author_email="renearteaga261998@gmail.com",
	license="GPLv3",
	include_package_data=True,
	packages=["RenePy"

		,"RenePy.ClasesUtiles"
		,"RenePy.ClasesUtiles.BasesDeDatos"
		,"RenePy.ClasesUtiles.BasesDeDatos.Factory"
		,"RenePy.ClasesUtiles.Interfaces"
		,"RenePy.ClasesUtiles.Tipos"
		,"RenePy.ClasesUtiles.Interfaces"
		,"RenePy.MetodosUtiles"
		,"RenePy.MetodosUtiles.Imports"],
	url="https://github.com/critBus/RenePython",
	classifiers = ["Programming Language :: Python :: 3",
	"License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
	"Development Status :: 4 - Beta", "Intended Audience :: Developers",
	"Operating System :: OS Independent"],
	
	)