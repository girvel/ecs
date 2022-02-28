import ecs

def test_creating():
    def protosystem(subject: "attribute1"):
        pass

    system = ecs.create_system(protosystem)
    
    assert system.process is protosystem
    assert system.ecs_targets is not None