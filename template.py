import itertools
import copy
import re
import pdb 

#import openai 

from fixtures.nps import NPS_MAP, PLURAL_NP_TO_SINGULAR
from fixtures.vps import VPS_MAP

CONN_MAP = {"and": "AND", "or": "OR", "if": "IMPLY", "only if": "IFF"}

class Template:
    def __init__(self, 
                 template_list,
                 template_tags):
        # a template list is a mixed type list of strings and lists of options
        self.template_list = template_list
        self.template_tags = template_tags

        self.denotation_lookup = NPS_MAP
        self.denotation_lookup.update(VPS_MAP)
        self.denotation_lookup.update(CONN_MAP)

        for k, v in self.denotation_lookup.items():
            if type(v) == str:
                self.denotation_lookup[k] = [v]

        if len(self.template_list) != len(self.template_tags):
            raise Exception("template list and template tags must be same length")

        for i, element in enumerate(self.template_list):
            if not isinstance(element, list):
                self.template_list[i] = [element]
                # make sure tag is None
                if isinstance(self.template_tags[i], str):
                    raise Exception("template tag must be None if template element is not a list")

    def product(self, *lists):
        def is_repeat(item, result, pool):
            # if singleton pool, then no repeats
            if len(pool) == 1:
                return False
            return item in result

        # like itertools.product but do not allow duplicate elements anywhere
        # e.g. product([1,2], [1,2]) = [(1,2), (2,1), (2,2)]
        result = []
        pools = [tuple(pool) for pool in lists] 
        result = [[]]
        for pool in pools:
            result = [x+[y] for x in result for y in pool if not is_repeat(y, x, pool)]
        for prod in result:
            yield tuple(prod)

    def expand_template(self):
        all_options = [x for x in self.product(*self.template_list)]
        return all_options

    def generate(self, lf_template, template_idx, amb_type):
        # generate iterates through template list and generates all possible combinations of strings
        all_surface = self.expand_template()
        # get LF for each surface form

        pairs = []
        for surface in all_surface:
            var_bindings = []
            lf_template_copy = copy.deepcopy(lf_template)
            # fill variables
            for i, token in enumerate(surface):
                if self.template_tags[i] is not None:
                    tag = self.template_tags[i]
                    denotations = self.denotation_lookup[token]
                    # if there are multiple denotations, then we need to fill in multiple times
                    var_bindings.append((tag, denotations))

            product_of_options = [x for x in itertools.product(*[x[1] for x in var_bindings])]
            tags = [x[0] for x in var_bindings]
            all_var_bindings = []

            for product in product_of_options:
                binding = {}
                for i, tok in enumerate(product):
                    tag = tags[i]
                    binding[tag] = tok
                all_var_bindings.append(binding)

            surface = self.make_fluent(surface)

            for var_binding in all_var_bindings:
                filled = lf_template_copy.format(**var_binding)

                data = {"surface": surface, 
                        "lf": filled, 
                        "unfilled_template": lf_template,
                        "template_tags": self.template_tags,
                        "var_bindings": var_binding,
                        "template_idx": template_idx,
                        "type": amb_type}
                pairs.append(data) 

        return pairs 

    def make_fluent(self, surface):
        """some simple rules to make the surface fluent"""
        # check for invalid plurals
        force_singular = ['a', 'every', 'each', 'the']
        surface = list(surface)
        for i, word in enumerate(surface):
            if word in PLURAL_NP_TO_SINGULAR.keys() and i > 0:
                prev_word = surface[i-1]
                if prev_word in force_singular:
                    surface[i] = PLURAL_NP_TO_SINGULAR[word]

        # create string 
        surface = " ".join(surface)
        # check for invalid articles
        a_an_gex = re.compile(r'(^| )(a) ([aeiou])')
        surface = re.sub(a_an_gex, r'\1\2n \3', surface)
        return surface
    

VAR_MAPPING = {"np1": "NOUN1", "np2": "NOUN2", "np3": "NOUN3", "vp1": "VERB1", "vp2": "VERB2", "vp3": "VERB3"}
REVERSE_VAR_MAPPING = {v:k for k,v in VAR_MAPPING.items()}

# class ModelTemplate(Template):

#     def verbalize(self):
#         # see which format variables lf_template contains
#         text = []
#         for tag, word in zip(self.template_tags, self.template_list):
#             if tag is None:
#                 text.append(word[0]) 
#             else:
#                 text.append(tag)
        
#         template = " ".join(text)
#         for var in VAR_MAPPING.keys():
#             template = re.sub(var, VAR_MAPPING[var], template)

#         return template
    
#     def parse_output(self, output):
#         # parse into sentence and variables 
#         split_output = output.strip().split("\n")
#         sent_line = split_output[0]
#         var_lines = split_output[1:]
#         sent_line = re.sub("SENTENCE: ", "", sent_line).strip()
#         binding = {}
#         for vl in var_lines:
#             var, rest = vl.split(":")
#             varname = REVERSE_VAR_MAPPING[var.strip()]
#             binding[varname] = rest.strip() 
#         return sent_line, binding

#     def generate(self, lf_template, template_idx, amb_type, n=20):
#         verbalized_template = self.verbalize()
#         all_surface = self.expand_template()
#         # get variable bindings for example 
#         # surface = " ".join(all_surface[0]) 
#         surface = all_surface[0]
#         _var_bindings = []
#         for i, token in enumerate(surface):
#             if self.template_tags[i] is not None:
#                 tag = self.template_tags[i]
#                 denotations = self.denotation_lookup[token]
#                 # if there are multiple denotations, then we need to fill in multiple times
#                 _var_bindings.append((tag, denotations))
#         product_of_options = [x for x in itertools.product(*[x[1] for x in _var_bindings])]
#         tags = [x[0] for x in _var_bindings]
#         all_var_bindings = []
#         for product in product_of_options:
#             binding = {}
#             for i, tok in enumerate(product):
#                 tag = tags[i]
#                 binding[tag] = tok
#             all_var_bindings.append(binding)
#         var_binding = all_var_bindings[0]
#         binding_str = [f"{VAR_MAPPING[k]}: {v}" for k, v in var_binding.items()]
#         binding_str = "\n".join(binding_str)

#         surface_str = " ".join(surface)
#         example = f"SENTENCE: {surface_str}\n{binding_str}"
#         vars = var_binding.keys()
#         tag_str = "\n".join([f"{VAR_MAPPING[v]}: <{VAR_MAPPING[v].lower()}>" for v in vars])

#         # make a prompt and generate 
#         prompt = f"""Please help me create some example sentences. I will give you a template and ask you to fill in the blanks in the template. 
# The template is: "{verbalized_template}".
# Give your answer as 
# SENTENCE: <sentence>
# {tag_str}
# with no other text whatsoever.
# Example:
# {example}"""
#         pdb.set_trace()
#         result = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             messages=[{"role": "user", "content": prompt}],
#             temperature=0.2,
#             n = n,
#             )
        
#         pairs = []
#         for output in result.choices:

#             lf_template_copy = copy.deepcopy(lf_template)
#             output = output.message.content
#             sent, binding = self.parse_output(output)
#             filled = lf_template_copy.format(**binding)

#             data = {"surface": sent, 
#                     "lf": filled, 
#                     "unfilled_template": lf_template,
#                     "template_tags": self.template_tags,
#                     "var_bindings": binding,
#                     "template_idx": template_idx,
#                     "type": amb_type}
            
#             pairs.append(data)
#         return pairs 
         
