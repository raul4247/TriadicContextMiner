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
        self.generators = {}

    # Save dyadic context into file
    def save(self, file_path):
        file = open(file_path, "w", encoding='utf-8')

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
        file = open(file_name, 'r', encoding='utf-8')

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

    # Find superior concepts for an intent's set
    def find_superior_concepts(self, intent_set):
        linked = []

        for link in self.links:
            if intent_set == link[0] or intent_set == link[1]:
                linked.append(link)

        concepts = []
        intent_len = len(self.concepts_reverse[frozenset(intent_set)])

        for link in linked:
            if link[0] == intent_set and frozenset(link[1]) in self.concepts_reverse:
                if len(self.concepts_reverse[frozenset(link[1])]) > intent_len:
                    concepts.append(link[1])

            if link[1] == intent_set and frozenset(link[0]) in self.concepts_reverse:
                if len(self.concepts_reverse[frozenset(link[0])]) > intent_len:
                    concepts.append(link[0])

        return concepts

    # Find all objects that contains one intent's set
    def derive_attributes(self, attributes):
        extent_set = frozenset({})

        for extent, intent in self.concepts.items():
            if attributes <= intent:
                extent_set |= extent

        if 'ø' in extent_set:
            extent_set -= {'ø'}
        return extent_set

    # update generators for single concept
    def update_feature_generators(self, concept, sup_intent):
        face = concept['attributes'] - sup_intent

        if concept['attributes'] not in self.generators:
            self.generators[concept['attributes']] = [frozenset({f}) for f in face]
        else:
            new_gen = []
            diff_gen = []
            for g in self.generators[concept['attributes']]:
                if len(g & face) != 0:
                    new_gen.append(g)
                else:
                    diff_gen.append(g)

            keep_gen = new_gen.copy()

            if len(diff_gen) == 0:
                diff_gen.append(frozenset({}))

            for g in diff_gen:
                for element in face:
                    keep = True
                    g_sup = g | frozenset({element})
                    for keep_set in keep_gen:
                        if keep_set <= g_sup:
                            keep = False
                            break
                    if keep:
                        new_gen.append(g_sup)

                self.generators[concept['attributes']] = new_gen

    # Compute feature generators for context concepts
    def compute_feature_generators(self):
        first_concept = True
        for extent, intent in self.concepts.items():
            if first_concept:
                self.generators[intent] = [frozenset({i}) for i in intent]
                first_concept = False
            else:
                sup_concepts = self.find_superior_concepts(intent)
                for concept in sup_concepts:
                    self.update_feature_generators({'objects': extent, 'attributes': intent}, concept)

        for concept_intent, concept_generators in self.generators.items():
            final_generators_set = []
            for g in concept_generators:
                if self.derive_attributes(g) == self.concepts_reverse[concept_intent]:
                    final_generators_set.append(g)

            self.generators[concept_intent] = final_generators_set

    # Save concepts links into file
    def save_links(self, file_path):
        file = open(file_path, 'w', encoding='utf-8')

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

    # Shows the generators count
    def show_generators_count(self):
        gen_count = sum(len(g) for g in self.generators)
        print('{0} generators found'.format(gen_count))
