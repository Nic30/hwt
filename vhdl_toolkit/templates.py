from jinja2 import Environment, PackageLoader


class VHDLTemplates(object):
    '''
    Class for loading vhdl templates
    '''
    env = Environment(loader=PackageLoader('vhdl_toolkit', 'templates_vhdl'))
    architecture = env.get_template('architecture.vhd')
    entity = env.get_template('entity.vhd')
    process = env.get_template('process.vhd')
        
        
        
