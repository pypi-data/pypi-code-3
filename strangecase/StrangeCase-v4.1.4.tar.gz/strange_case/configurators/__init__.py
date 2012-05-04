from functools import wraps

from strange_case.registry import Registry


def provides(conf):
    def decorator(function):
        @wraps(function)
        def wrapper(source_file, config):
            if conf not in config:
                return function(source_file, config)
            return config
        return wrapper
    return decorator


def configurate(source_file, config):
    verbose = config.get('verbose')
    configurators = Registry.configurators
    # Run the config through each configurator.
    # If a configurator returns a falsey
    # value, the node will be ignored.
    for configurator in configurators:
        config = configurator(source_file, config)
        if not config:
            if verbose:
                print 'Ignoring "{0}" due to configurator {1}'.format(source_file, configurator.__name__)
            return
    return config


def meta_before(source_file, config):
    configurators = Registry.configurators
    for configurator in configurators:
        if hasattr(configurator, 'defaults'):
            for key, value in configurator.defaults.iteritems():
                if key not in config:
                    config[key] = value

        if hasattr(configurator, 'require_before'):
            for required in configurator.require_before:
                if required not in config:
                    raise TypeError('Missing required config["{required}"] '
                        'from {configurator.__name__}.require_before'.format(**locals()))
    return config


def meta_after(source_file, config):
    configurators = Registry.configurators
    for configurator in configurators:
        if hasattr(configurator, 'require_after'):
            for required in configurator.require_after:
                if required not in config:
                    raise TypeError('Missing required config["{required}"] '
                        'from {configurator.__name__}.require_after'.format(**locals()))
    return config


from dont_inherit import dont_inherit
from file_types import file_types
from folder_config_file import folder_config_file
from front_matter_config import front_matter_config
from ignore import ignore
from is_index import is_index
from merge_files_config import merge_files_config
from setdefault_name import setdefault_name
from setdefault_target_name import setdefault_target_name
from set_url import set_url
from setdefault_iterable import setdefault_iterable
from skip_if_not_modified import skip_if_not_modified
