# -*- coding: utf-8 -*-
import os


class DyadicContext:
    def __init__(self, context, objects_count, attributes_count):
        self.context = context
        self.objects_count = objects_count
        self.attributes_count = attributes_count
        self.concepts = {}
        self.concepts_reverse = {}
        self.links = []

    # Save dyadic context into file
    def save(self, file_path):
        file = open(file_path, "w")

        for obj, attrs in self.context.items():
            file.write(obj + " ")
            attr_str = ""

            for attr in attrs:
                attr_str += attr + ","

            file.write(attr_str[:-1] + "\n")
        file.close()

    # Uses data-peeler to mine concepts
    @staticmethod
    def mine_concepts(dyadic_context_file, output_concepts_file):
        os.system('d-peeler {0} --out {1}'.format(dyadic_context_file, output_concepts_file))

    # Read concepts from file
    def read_concepts_from_file(self, file_name):
        file = open(file_name, 'r')

        self.concepts = {}
        self.concepts_reverse = {}

        for line in file.readlines():
            obj = frozenset(line.split(' ')[0].split(','))
            attr = frozenset([a.rstrip('\n') for a in line.split(' ')[1].split(',')])

            self.concepts.update({obj: attr})
            self.concepts_reverse.update({attr: obj})

    # Run iPred algorithm to mine links between concepts
    def iPred(self):
        attributes = self.concepts.values()
        attributes = [i for i in attributes]

        if frozenset({'ø'}) not in attributes:
            attributes.append(frozenset({'ø'}))

        attributes.sort(key=len)

        empty_set = {'ø'}
        faces = {}
        links = []

        for i in attributes:
            faces[i] = empty_set

        border = attributes.pop(0)

        for Ci in attributes:
            candidates = set({})

            for element in border:
                candidates = candidates | frozenset({(Ci & frozenset(element))})

            candidates = (candidates - frozenset({frozenset({})})) | empty_set

            for element in candidates:
                delta_intersection = Ci & faces[frozenset(element)]
                if len(delta_intersection) == 0 or delta_intersection == empty_set:
                    links.append([Ci, set(element)])
                    faces[frozenset(element)] = (faces[frozenset(element)] | (Ci - set(element))) - empty_set
                    border = (border - frozenset({element})) - empty_set

            border = border | {Ci}

        self.links = links

    # Save concepts links into file
    def save_links(self, file_path):
        file = open(file_path, 'w')

        for link in self.links:
            if frozenset(link[0]) in self.concepts_reverse.keys() and frozenset(
                    link[1]) in self.concepts_reverse.keys():

                for i in sorted(self.concepts_reverse[frozenset(link[0])]):
                    file.write(str(i) + ' ')

                file.write('<---> ')

                for i in sorted(self.concepts_reverse[frozenset(link[1])]):
                    file.write(str(i) + ' ')

                file.write('\n')

    # Shows the context size
    def show_size(self):
        print('{0} Objects'.format(self.objects_count))
        print('{0} Attributes'.format(self.attributes_count))

    # Shows the concepts count
    def show_concepts_count(self):
        print('Mined {0} concepts'.format(len(self.concepts)))

    # Shows the links count
    def show_links_count(self):
        print('{0} links found between concepts'.format(len(self.links)))

