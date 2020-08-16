# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np


class TriadicContext(object):

    # Uses pandas to read a triadic context input from a csv file
    @staticmethod
    def read_triadic_context(file_name):
        data_frame = pd.read_csv(file_name, sep=" ", header=None, low_memory=False)
        data_frame.columns = ["Extent", "Intent", "Modus"]

        return data_frame

    # Convert a triadic context to a dyadic one by flattening the third dimension
    @staticmethod
    def to_dyadic(triadic_context):
        context = {}
        intents = []

        for index, row in triadic_context.iterrows():
            extent = str(row['Extent'])
            intent = str(row['Intent'])
            if extent not in context:
                context[extent] = []

            for modus in str(row['Modus']).split(","):
                new_intent = intent + modus
                if new_intent not in context[extent]:
                    context[extent].append(new_intent)

                if new_intent not in intents:
                    intents.append(new_intent)

        objects_count = len(context.items())
        attributes_count = len(intents)

        return context, objects_count, attributes_count

    # Shows the context size
    @staticmethod
    def show_size(context):
        objects_len = len(np.unique(np.array(context['Extent'])))
        attributes_len = len(np.unique(np.array(context['Intent'])))
        conditions_len = len(np.unique(np.array(context['Modus'])))

        print('{0} Objects'.format(objects_len))
        print('{0} Attributes'.format(attributes_len))
        print('{0} Conditions'.format(conditions_len))

        return objects_len, attributes_len, conditions_len
