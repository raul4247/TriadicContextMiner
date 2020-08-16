# -*- coding: utf-8 -*-
import os
from tqdm import tqdm


class DyadicContext:
    def __init__(self, context, objects_count, attributes_count):
        self.context = context
        self.objects_count = objects_count
        self.attributes_count = attributes_count
        self.concepts = {}
        self.concepts_reverse = {}
        self.links = []
        self.generators = {}
        self.rules = []

    # Save dyadic context into file
    def save_context(self, file_path):
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

        for Ci in tqdm(attributes):
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
        linked = [link for link in self.links if intent_set == link[0] or intent_set == link[1]]

        concepts = []
        intent_len = len(self.concepts_reverse[frozenset(intent_set)])

        if self.concepts_reverse[frozenset(intent_set)] == frozenset({'ø'}):
            for link in linked:
                if link[0] == intent_set and frozenset(link[1]) in self.concepts_reverse:
                    concepts.append(link[1])
                if link[1] == intent_set and frozenset(link[0]) in self.concepts_reverse:
                    concepts.append(link[0])
        else:
            for link in linked:
                if link[0] == intent_set and frozenset(link[1]) in self.concepts_reverse:
                    if len(self.concepts_reverse[frozenset(link[1])]) > intent_len:
                        concepts.append(link[1])

                if link[1] == intent_set and frozenset(link[0]) in self.concepts_reverse:
                    if len(self.concepts_reverse[frozenset(link[0])]) > intent_len:
                        concepts.append(link[0])

        return concepts

    # Find inferior concepts for an intent's set
    def find_inferior_concepts(self, intent_set):
        linked = [link for link in self.links if intent_set == link[0] or intent_set == link[1]]

        concepts = []
        intent_len = len(self.concepts_reverse[frozenset(intent_set)])

        for link in linked:
            if link[0] == intent_set and frozenset(link[1]) in self.concepts_reverse:
                if len(self.concepts_reverse[frozenset(link[1])]) < intent_len:
                    concepts.append(link[1])

            if link[1] == intent_set and frozenset(link[0]) in self.concepts_reverse:
                if len(self.concepts_reverse[frozenset(link[0])]) < intent_len:
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
        for extent, intent in tqdm(self.concepts.items()):
            if first_concept:
                self.generators[intent] = [frozenset({i}) for i in intent]
                first_concept = False
            else:
                sup_concepts = self.find_superior_concepts(intent)
                for concept in sup_concepts:
                    self.update_feature_generators({'objects': extent, 'attributes': intent}, concept)

        for concept_intent, concept_generators in tqdm(self.generators.items()):
            final_generators_set = []

            for g in concept_generators:
                if self.derive_attributes(g) == self.concepts_reverse[concept_intent]:
                    final_generators_set.append(g)
                if len(self.derive_attributes(g)) == 0 and self.concepts_reverse[
                    frozenset(concept_intent)] == frozenset({'ø'}):
                    final_generators_set.append(g)
            self.generators[concept_intent] = final_generators_set

    # Lattice Miner Implementation
    def LM_update_feature_generators(self, concept):
        generators = []

        if len(concept['attributes']) > 0:
            parents_intents = self.find_superior_concepts(concept['attributes'])
            faces = []
            for i in parents_intents:
                faces.append(concept['attributes'] - i)

            if len(faces) > 0:
                first_face = faces.pop(0)
                for f in first_face:
                    generators.append(frozenset({f}))

                if len(faces) > 0:
                    for f in faces:
                        min_blockers = []
                        blockers = []

                        for g in generators:
                            if len(g & f) == 0:
                                for element in f:
                                    union = frozenset({element}) | g
                                    if union not in blockers:
                                        blockers.append(union)
                            else:
                                if frozenset(g) not in min_blockers:
                                    min_blockers.append(frozenset(g))

                        if len(blockers) == 0:
                            generators = min_blockers
                        elif len(min_blockers) == 0:
                            generators = blockers
                        else:
                            result = []
                            for b in blockers:
                                for min_b in min_blockers:
                                    if min_b <= b:
                                        if b not in result:
                                            result.append(b)
                                            break
                            generators = list(frozenset(min_blockers) | (frozenset(blockers) - frozenset(result)))
        else:
            generators = frozenset([i for i in concept['attributes']])

        return generators

    # Lattice Miner Implementation
    def LM_compute_feature_generators(self):
        first_concept = True
        for extent, intent in tqdm(self.concepts.items()):
            if first_concept:
                self.generators[intent] = [frozenset({i}) for i in intent]
                first_concept = False
            else:
                self.generators[intent] = self.update_feature_generators({'objects': extent, 'attributes': intent})

    # Compute the association rules
    def compute_association_rules(self):
        rules = []
        for concept_extent, concept_intent in tqdm(self.concepts.items()):
            if concept_intent in self.generators:

                ant_support = len(concept_extent) / self.objects_count
                children = self.find_inferior_concepts(concept_intent)

                for g in self.generators[concept_intent]:
                    if len(children) != 0 and len(concept_intent) != 0:
                        for child_intent in children:
                            child_extent = self.concepts_reverse[child_intent]
                            cons_support = len(child_extent) / self.objects_count

                            potential_cons = [i for i in child_intent if i not in concept_intent]

                            rule_conf = cons_support / ant_support

                            if len(potential_cons) != 0:
                                rule = {"generator": g, "potential_cons": potential_cons, "support": cons_support,
                                        "confidence": rule_conf}
                                rules.append(rule)

                    rule_support = len(concept_extent) / self.objects_count
                    potential_cons = [i for i in concept_intent if i not in g]

                    if len(potential_cons) != 0:
                        rule = {"generator": g, "potential_cons": potential_cons, "support": rule_support,
                                "confidence": 1.0}
                        rules.append(rule)

        self.rules = rules

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

        file.close()

    # Save generators into file
    def save_generators(self, file_path):
        file = open(file_path, 'w', encoding='utf-8')

        for intent, generator in self.generators.items():
            file.write(
                str([set(i) for i in self.concepts_reverse[intent]]) + ' -> ' + str([set(i) for i in generator]) + '\n')

        file.close()

    # Save concepts links into file
    def save_rules(self, file_path):
        file = open(file_path, 'w', encoding='utf-8')

        for rule in self.rules:
            file.write(str([set(i) for i in rule['generator']]) + ' ->' + str(
                [set(i) for i in rule['potential_cons']]) + '\n')
            file.write('Support: {0}\t Confidence: {1}\n\n'.format(rule['support'], rule['confidence']))

        file.close()

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

    # Shows the rules count
    def show_rules_count(self):
        print('{0} rules computed'.format(len(self.rules)))
