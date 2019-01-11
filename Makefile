##
## Makefile for Makefile in /home/jean.walrave/projects/epitech/autoCompletion_2016
##
## Made by Jean Walrave
## Login   <jean.walrave@epitech.net>
##
## Started on  Thu Jul  6 08:13:42 2017 Jean Walrave
## Last update Sun Jul  9 10:36:31 2017 Jean Walrave
##

PROJECT		= autoCompletion

SOURCES_PATH	= sources

all: $(PROJECT)

$(PROJECT):
		ln -s $(SOURCES_PATH)/$(PROJECT).py $(PROJECT)

clean:
		rm -rf $(SOURCES_PATH)/*.pyc
		rm -rf $(SOURCES_PATH)/*.pyo
		rm -rf $(SOURCES_PATH)/__pycache__/

fclean: clean
	rm -rf $(PROJECT)

re: fclean all

.PHONY: all clean fclean re
