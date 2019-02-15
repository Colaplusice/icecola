def fix_require(file_path):
    opener = open(file_path, 'r')
    lines = opener.readlines()
    new_line = [line.split('==')[0]+'\n' for line in lines]
    opener.close()
    with open(file_path, 'w')as opener:
        opener.writelines(new_line)


if __name__ == '__main__':
    fix_require('/Users/fjl2401/Documents/python/code/flask_proj/flask_receipe_app/requirements.txt')
