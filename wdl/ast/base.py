class ASTNode:
    def __init__(self, children=None, leaf=None):
        self.children = children if children else []
        self.leaf = leaf
        self.pos = None

    def __str__(self):
        return self.__class__.__name__

    def set_span(self, start_pos, end_pos):
        self.start_pos = start_pos
        self.end_pos = end_pos

    def to_dict(self):
        return {
            'type': self.__class__.__name__,
            'children': [child.to_dict() for child in self.children] if self.children else [],
            'leaf': self.leaf,
            'span': (self.start_pos, self.end_pos)
        }

class RootNode(ASTNode):
    def __init__(self, main_body):
        super().__init__(children=main_body)
        self.main_body = main_body
