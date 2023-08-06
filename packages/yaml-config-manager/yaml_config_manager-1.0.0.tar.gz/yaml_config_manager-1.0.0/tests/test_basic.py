from yaml_config_manager import YamlConfig

YAML_FILE = 'config.yml'

def test_sanity():
    conf = YamlConfig(YAML_FILE)

    assert conf.key == 'value'
    assert conf.mysqldatabase.hostname == 'localhost'
    assert type(conf.mysqldatabase.port) == int
    assert not conf.booleanValue