from setuptools import setup
import os

def read_file(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as file:
        return file.read()

setup(
  name = 'multi-agent-decision',         
  packages = ['multi_agent_decision'],   
  version = '0.1',      
  license='MIT',        
  description = 'Simulates the actions which agents take under multi-agent systems and social networks',  
  long_description=read_file('README.md'),
  long_description_content_type='text/markdown',  
  author = 'ankurtutlani',                   
  author_email = 'ankur.tutlani@gmail.com',      
  url = 'https://github.com/ankur-tutlani/multi-agent-decision',   
  download_url = 'https://github.com/ankur-tutlani/multi_agent_decision/archive/refs/tags/v_01.tar.gz',    
  keywords = ['game theory', 'evolutionary game', 'social norms','multi-agent systems','evolution','social network','computational economics','simulation','agent-based modeling','computation'],   
  install_requires=[            
          'numpy',
		  'pandas',
		  'networkx',
		  'matplotlib',
		  'setuptools'
		  
		  
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
												
	'Programming Language :: Python :: 3.7',
  ],
)