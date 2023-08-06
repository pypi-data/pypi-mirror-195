from setuptools import setup
setup(

	name="ReneTkinter",
	version="1.0",
	description="visual de Python",
	author="René Lázaro Collado Arteaga",
	author_email="renearteaga261998@gmail.com",
	license="GPLv3",
	include_package_data=True,
	packages=["Tkinters"
		,"Tkinters.ClasesUtiles"
		,"Tkinters.ClasesUtiles.Tipos"
		,"Tkinters.ClasesUtiles.Componentes"
		,"Tkinters.ClasesUtiles.Interfaces"
		,"Tkinters.Imports"],
	url="https://github.com/critBus/ReneTkinter",
	classifiers = ["Programming Language :: Python :: 3",
	"License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
	"Development Status :: 4 - Beta", "Intended Audience :: Developers",
	"Operating System :: OS Independent"],
	
	)