from platform import system

# OS를 확인한다.
if system() == "Windows":
    dir_delimiter = "\\"
else:
    dir_delimiter = "/"
