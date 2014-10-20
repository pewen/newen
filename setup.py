from setuptools import setup

#Tengo que probar de alguna forma que esta instalado git y R

setup(
			name='Newen',
      version='0.1',
      description='Analisis estadistico de la energía eolica',
      author='Franco N. Bellomo',
      author_email='fnbellomo@gmail.com',
      url='https://pewen.github.io/',
      license='MIT',
      install_requires=['Flask >= 0.10', 
      									'numpy >= 1.7', 
      									'scipy >= 0.12', 
      									'pandas >= 0.12', 
      									'rpy2 >= 2.3',
      ],
     )
