import setuptools # Импорт недавно установленного пакета setuptools.
with open("README.md", "r") as fh: 
	long_description = fh.read() # Выбор описания
setuptools.setup(
	name="Neuro_fuzzy_EVAMortus", # Уникальное имя дистрибутива
	version="0.0.2", 	# Номер версии библиотеки
	author="Ermakov Vitaliy", # Имя автора.
	author_email="blackcheshireshusband@yandex.ru", # Почта автора
	description="Fuzzy output module", # Краткое описание
	long_description=long_description, 	# Длинное описание
	long_description_content_type="text/markdown", # Тип long_description
	url="", 	# Домашняя страница проекта
	packages=setuptools.find_packages(), # Объединение всех пакетов проекта
	install_requires=[], # Зависимости пакета	
classifiers=[ # Метаданные пакета
		"Programming Language :: Python :: 3.10",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.10', # Требуемая версия Python.
)
