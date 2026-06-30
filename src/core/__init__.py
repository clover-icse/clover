def get_task(name):
    if name == 'loop':
        from core.loop import LoopInvSolver
        return LoopInvSolver()
    else:
        raise NotImplementedError