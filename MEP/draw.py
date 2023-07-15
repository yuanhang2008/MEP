# -*- coding: utf-8 -*-


import matplotlib.pyplot as plt


class Config:

    def __init__(self, **kwargs):
        self.line_color: str = '#000000'
        self.line_style: str = 'solid'
        self.line_width: int | float = 2
        self.label: str = self.line_color
    
        self.overwrite(**kwargs)

    def overwrite(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise ValueError(f'{key} is not configurable')

DEFAULT_CONFIG = Config()

class Drawer:

    def __init__(self, max: int | None=None):
        self.max = max
        self.funcs = []

    def add_func(self, func, range_, config=DEFAULT_CONFIG):
        self.check_flow(self.max, len(self.funcs) + 1)
        self.funcs.append((func, range_, config))

    def check_flow(self, max, funcs_length) -> None:
        if max is None:
            return
        if funcs_length > max:
            raise ValueError(f'{funcs_length} (more than {max}) items to draw')

    def show(self):
        for func in self.funcs:
            func_ = func[0]
            range_ = func[1]
            config: Config = func[2]

            x = [item for item in range(*range_)]
            y = [func_(arg) for arg in x]
            
            plt.plot(x, y, 
            linewidth=config.line_width, 
            color=config.line_color, 
            linestyle=config.line_style)
        plt.show()