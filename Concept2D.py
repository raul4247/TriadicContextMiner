class Concept2D:
    def __init__(self, extent, intent):
        self.extent = extent
        self.intent = intent
        self.parents = []
        self.children = []

    def __hash__(self):
        return hash(self.extent) + hash(self.extent)

    def add_connection(self, other_concept):
        self_length = len(self.extent)
        other_length = len(other_concept.extent)

        if self.extent == frozenset({'ø'}):
            self_length -= 1

        if other_concept.extent == frozenset({'ø'}):
            other_length -= 1

        if self_length > other_length:
            self.children.append(other_concept)
            other_concept.parents.append(self)
        elif other_length > self_length:
            other_concept.children.append(self)
            self.parents.append(other_concept)
