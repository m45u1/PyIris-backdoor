import library.modules.dynamic_help_generator as dynamic_help_generator
import library.modules.compiler as compiler
import library.modules.config as config
import library.modules.clean_import_data as clean_import_data
import os

config.main()
tmp_win = config.win_components.values()
tmp_win.append('windows/base')
for i in tmp_win:
    exec ('import components.' + i.replace('/', '.') + ' as ' + i.replace('/', '_'))
print config.pos + 'Loaded all windows components into generator - OK'
tmp_lin = config.lin_components.values()
tmp_lin.append('linux/base')
for i in tmp_lin:
    exec ('import components.' + i.replace('/', '.') + ' as ' + i.replace('/', '_'))
print config.pos + 'Loaded all linux components into generator - OK'


def main():
    original = os.getcwd()
    os.chdir(config.started_at)
    comp_list = sorted([i for i in config.loaded_components.values() if not i.endswith('/base')])
    for i in config.loaded_components.values():
        if i.endswith('/base'):
            comp_list.insert(0, i)
    for i in comp_list:
        print config.pos + 'Loading and executing : ' + i
        exec (i.replace('/', '_') + '.main("generate")')
    print config.inf + 'Reading contents from temporary written file...'
    f = open(config.scout_values['Path'][0], 'r')
    save_data = f.read()
    f.close()
    config.functions = list(set(config.functions))
    config.import_statements = list(set(config.import_statements))
    config.global_objs = list(set(config.global_objs))
    config.logics = list(set(config.logics))
    f = open(config.scout_values['Path'][0], 'w')
    print config.inf + 'Writing in imports...'
    f.write(clean_import_data.main(config.import_statements) + '\n\n')
    print config.inf + 'Writing in help menu...'
    f.write('help_menu = ' + "'''" + dynamic_help_generator.main() + "'''" + '\n')
    print config.inf + 'Writing in global variables...'
    for i in config.global_objs:
        f.write(i + '\n')
    print config.inf + 'Writing in components...'
    for i in config.functions:
        f.write(i + '\n')
    print config.inf + 'Writing in startup components...'
    for i in config.startup:
        f.write(i + '\n')
    for i in config.startup_end:
        f.write(i + '\n')
    print config.inf + 'Writing in base component...'
    for i in config.logics:
        save_data = save_data.replace('#Statements#', '#Statements#' + i)
    save_data = save_data.replace('#Statements#', '')
    f.write(save_data)
    f.close()
    if config.scout_values['Compile'][0] == 'True':
        print config.inf + 'Compiling scout...'
        compiler.main(config.scout_values['Path'][0])
    print config.pos + 'Successfully generated scout python file to : ' + os.path.join(os.getcwd(),
                                                                                       config.scout_values['Path'][0])
    config.functions = []
    config.import_statements = []
    config.global_objs = []
    config.logics = []
    config.startup = []
    config.startup_end = []
    config.help_menu = {}
    os.chdir(original)