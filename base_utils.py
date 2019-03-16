def fix_require(file_path):
    '''
    fix pip auto generate requirements.txt
    rm package version to avoid version lock
    usage: fix_require('/Users/fjl2401/Documents/python/code/flask_proj/
    flask_recipe_app/requirements.txt')

    :param file_path:
    :return:
    '''
    opener = open(file_path, 'r')
    lines = opener.readlines()
    new_line = [line.split('==')[0] + '\n' for line in lines]
    opener.close()
    with open(file_path, 'w')as opener:
        opener.writelines(new_line)
