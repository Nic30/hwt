from jinja2 import Environment, PackageLoader

class VHDLTemplates(object):
    '''
    Class for loading vhdl templates
    '''
    env = Environment(loader=PackageLoader('hdl_toolkit', 'serializer/templates_vhdl'))
    architecture = env.get_template('architecture.vhd')
    entity = env.get_template('entity.vhd')
    process = env.get_template('process.vhd')
    component = env.get_template('component.vhd')
    componentInstance = env.get_template('component_instance.vhd')
    
    If = env.get_template('if.vhd')
    Switch = env.get_template('switch.vhd')
        
        
