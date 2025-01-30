import random
from fixtures.nps import (
    INDEFINITE_NPS,
    INDEFINITE_HUMAN_NPS,
    NAMES,
    MALE_NAMES,
    FEMALE_NAMES,
    INDEFINITE_MALE_NPS,
    INDEFINITE_FEMALE_NPS,
    VISUAL_INSTRUMENT_NPS,
    NONVISUAL_NPS,
    TACTILE_INSTRUMENT_NPS,
    INDEFINITE_SENTIENT_NPS,
    INDEFINITE_NONHUMAN_SENTIENT_NPS
)
from fixtures.vps import (
    VISUAL_VPS,
    TACTILE_VPS,
    INTRANSITIVE_VPS,
    TRANSITIVE_VPS,
    INTRANSITIVE_VPS_FOR_BOUND
)
from template import Template

#WITH TRANSLATIONS
def generate_xor_pairs():
    """
    generate pairs of sentences with conjunction ambiguities
    of the form:
    Either the man ate or drank and slept
        ( eat ( man ) XOR drink ( man ) ) AND sleep ( man )
        eat ( man ) XOR ( drink ( man ) AND sleep ( man ) )
    """
    pairs = []

    xor_and_template_text = ["either", "the", INDEFINITE_SENTIENT_NPS, INTRANSITIVE_VPS, "or", INTRANSITIVE_VPS, "and", INTRANSITIVE_VPS]
    xor_and_template_tags = [None, None, "np1", "vp1", None, "vp2", None, "vp3"]

    xor_and_template = Template(xor_and_template_text, xor_and_template_tags)

    xor_and_lf_template_1 = "{vp1} ( {np1} ) XOR ( {vp2} ( {np1} ) AND {vp3} ( {np1} ) )" # xor binds first
    xor_and_lf_template_2 = "( {vp1} ( {np1} ) XOR {vp2} ( {np1} ) ) AND {vp3} ( {np1} )" # and binds first
    
    # Generate pairs with translations for and_first template
    for i, (lf_template, idx) in enumerate([(xor_and_lf_template_1, 0), (xor_and_lf_template_2, 1)]):
        for pair in xor_and_template.generate(lf_template, idx, "conj"):
            np1 = pair["var_bindings"]["np1"]
            vp1 = pair["var_bindings"]["vp1"]
            vp2 = pair["var_bindings"]["vp2"]
            vp3 = pair["var_bindings"]["vp3"]

            # Create translations based on the logical form
            if idx == 0:
                translation = (
                    f"One of these two things happened: 1. The {np1} {vp1}. 2. The {np1} {vp2} and {vp3}."
                
                )
            else:
                translation = (
                    f"The {np1} definitely {vp3}. And one of these two things happened: 1. The {np1} {vp1}. 2. The {np1} {vp2}."
                )

            pair["translation"] = translation
            pairs.append(pair)
    return pairs

#WITH TRANSLATIONS
def generate_xor_pairs_different_nps():
    """
    generate pairs of sentences with conjunction ambiguities
    of the form:
    Either the man ate or the woman drank and the dog slept
        ( eat ( man ) XOR drink ( woman ) ) AND sleep ( dog )
        eat ( man ) XOR ( drink ( woman ) AND sleep ( dog ) )
    """
    pairs = []

    xor_and_template_text = ["either", "the", INDEFINITE_SENTIENT_NPS, INTRANSITIVE_VPS, "or", "the", INDEFINITE_SENTIENT_NPS, INTRANSITIVE_VPS, "and", "the", INDEFINITE_SENTIENT_NPS, INTRANSITIVE_VPS]
    xor_and_template_tags = [None, None, "np1", "vp1", None, None, "np2", "vp2", None, None, "np3", "vp3"]

    xor_and_template = Template(xor_and_template_text, xor_and_template_tags)

    xor_and_lf_template_1 = "{vp1} ( {np1} ) XOR ( {vp2} ( {np2} ) AND {vp3} ( {np3} ) )" # xor binds first
    xor_and_lf_template_2 = "( {vp1} ( {np1} ) XOR {vp2} ( {np2} ) ) AND {vp3} ( {np3} )" # and binds first


    for i, (lf_template, idx) in enumerate([(xor_and_lf_template_1, 0), (xor_and_lf_template_2, 1)]):
        for pair in xor_and_template.generate(lf_template, idx, "conj"):
            np1 = pair["var_bindings"]["np1"]
            vp1 = pair["var_bindings"]["vp1"]
            np2 = pair["var_bindings"]["np2"]
            vp2 = pair["var_bindings"]["vp2"]
            np3 = pair["var_bindings"]["np3"]
            vp3 = pair["var_bindings"]["vp3"]

            # Create translations based on the logical form
            if idx == 0:
                translation = (
                    f"One of these two things happened: 1. The {np1} {vp1} 2. The {np2} {vp2} and the {np3} {vp3}."
                )
            else:
                translation = (
                    f"The {np3} definitely {vp3}. And one of these two things happened: 1. The {np1} {vp1}. 2. The {np2} {vp2}."                      
                )

            pair["translation"] = translation
            pair["template_type"] = "and_first"
            pairs.append(pair)
    return pairs

#WITH TRANSLATIONS
def generate_scope_pairs():
    """
    generate pairs of sentences and LFs with scope ambiguities
    of the form:
    every man hears a bird
        ALL x ( man ( x ) -> EXISTS y ( bird ( y ) AND hear ( x , y ) ) )
        EXISTS y ( bird ( y ) -> ALL x ( man ( x ) AND hear ( x , y ) ) )
    """
    pairs = []
    
    every_template_text = ["every", INDEFINITE_SENTIENT_NPS, TRANSITIVE_VPS, "a", INDEFINITE_NPS]
    every_template_tags = [None, "np1", "vp1", None, "np2"]

    every_template = Template(every_template_text, every_template_tags)
    
    lf_template_1 = "ALL x ( {np1} ( x ) -> EXISTS y ( {np2} ( y ) AND {vp1} ( x , y ) ) )"
    lf_template_2 = "EXISTS y ( {np2} ( y ) -> ALL x ( {np1} ( x ) AND {vp1} ( x , y ) ) )"

    # Generate pairs with translations for every template
    for i, (lf_template, idx) in enumerate([(lf_template_1, 0), (lf_template_2, 1)]):
        for pair in every_template.generate(lf_template, idx, "conj"):
            np1 = pair["var_bindings"]["np1"]
            np2 = pair["var_bindings"]["np2"]
            vp1 = pair["var_bindings"]["vp1"]

            # Create translations based on the logical form
            if idx == 0:
                translation = (
                    f"Every {np1} {vp1} at least one {np2}"
                )
            else:
                translation = (
                    f"There is a {np2} that every {np1} {vp1}"
                )

            pair["translation"] = translation
            pair["template_type"] = "every"
            pairs.append(pair)

    each_template_text = ["each", INDEFINITE_SENTIENT_NPS, TRANSITIVE_VPS, "a", INDEFINITE_NPS]
    each_template_tags = [None, "np1", "vp1", None, "np2"]
    each_template = Template(each_template_text, each_template_tags)

    # Generate pairs with translations for each template
    for i, (lf_template, idx) in enumerate([(lf_template_1, 0), (lf_template_2, 1)]):
        for pair in each_template.generate(lf_template, idx, "conj"):
            np1 = pair["var_bindings"]["np1"]
            np2 = pair["var_bindings"]["np2"]
            vp1 = pair["var_bindings"]["vp1"]

            # Create translations based on the logical form
            if idx == 0:
                translation = (
                    f"Each {np1} {vp1} at least one {np2}"
                )
            else:
                translation = (
                    f"There is a {np2} that each {np1} {vp1}"
                )

            pair["translation"] = translation
            pair["template_type"] = "each"
            pairs.append(pair)

    return pairs 

#WITH TRANSLATIONS
def generate_reverse_scope_pairs():
    """
    generate pairs of sentences and LFs with scope ambiguities but with quants at the end
    of the form:
    a man heard every bird/a doctor lives in every city
        EXISTS x ( man ( x ) -> ALL y ( bird ( y ) AND hear ( x , y ) ) )
        ALL y ( bird ( y ) -> EXISTS x ( man ( x ) AND hear ( x , y ) ) )
    """
    pairs = []

    every_template_text = ["a", INDEFINITE_SENTIENT_NPS, TRANSITIVE_VPS, "every", INDEFINITE_NPS]
    every_template_tags = [None, "np1", "vp1", None, "np2"]
    every_template = Template(every_template_text, every_template_tags)
    
    lf_template_1 = "EXISTS x ( {np1} ( x ) -> ALL y ( {np2} ( y ) AND {vp1} ( x , y ) ) )"
    lf_template_2 = "ALL y ( {np2} ( y ) -> EXISTS x ( {np1} ( x ) AND {vp1} ( x , y ) ) )"
    
    # Generate pairs with translations for and_first template
    for i, (lf_template, idx) in enumerate([(lf_template_1, 0), (lf_template_2, 1)]):
        for pair in every_template.generate(lf_template, idx, "conj"):
            np1 = pair["var_bindings"]["np1"]
            np2 = pair["var_bindings"]["np2"]
            vp1 = pair["var_bindings"]["vp1"]

            # Create translations based on the logical form
            if idx == 0:
                translation = (
                    f"There is a {np1} who {vp1} every {np2}"
                )
            else:
                translation = (
                    f"Every {np2} was {vp1} by at least one {np1}"
                )

            pair["translation"] = translation
            pair["template_type"] = "every"
            pairs.append(pair)

    each_template_text = ["a", INDEFINITE_SENTIENT_NPS, TRANSITIVE_VPS, "each", INDEFINITE_NPS]
    each_template_tags = [None, "np1", "vp1", None, "np2"]
    each_template = Template(each_template_text, each_template_tags)

    # Generate pairs with translations for and_first template
    for i, (lf_template, idx) in enumerate([(lf_template_1, 0), (lf_template_2, 1)]):
        for pair in each_template.generate(lf_template, idx, "conj"):
            np1 = pair["var_bindings"]["np1"]
            np2 = pair["var_bindings"]["np2"]
            vp1 = pair["var_bindings"]["vp1"]

            # Create translations based on the logical form
            if idx == 0:
                translation = (
                    f"There is a {np1} who {vp1} each {np2}"
                )
            else:
                translation = (
                    f"Each {np2} was {vp1} by at least one {np1}"
                )

            pair["translation"] = translation
            pair["template_type"] = "each"
            pairs.append(pair)

    return pairs 

#def generate_bound_pronoun_pairs(gender):
    """
    generate ambiguous pairs with bound gendered pronouns
    i.e.
    "Bill saw John and he waved"
    "The woman observed Mary and she left"
    """
    def generate_animate(name_choices, indef_choices, conj_statement):

        pairs = []

        def_def_template_text = [name_choices, VISUAL_VPS, name_choices, conj_statement, INTRANSITIVE_VPS_FOR_BOUND]
        def_def_template_tags = ["np1", "vp1", "np2", None, "vp2"]
        def_def_template = Template(def_def_template_text, def_def_template_tags)
        lf_template_1  = "{vp1} ( {np1}, {np2} ) AND {vp2} ( {np1} )" # (s)he = np1
        lf_template_2  = "{vp1} ( {np1}, {np2} ) AND {vp2} ( {np2} )" # (s)he = np2

        pairs += def_def_template.generate(lf_template_1, 0, "bound")
        pairs += def_def_template.generate(lf_template_2, 1, "bound")

        indef_def_template_text = ["the", indef_choices, VISUAL_VPS, name_choices, conj_statement, INTRANSITIVE_VPS_FOR_BOUND]
        indef_def_template_tags = [None, "np1", "vp1", "np2", None, "vp2"]
        indef_def_template = Template(indef_def_template_text, indef_def_template_tags)

        pairs += indef_def_template.generate(lf_template_1, 0, "bound")
        pairs += indef_def_template.generate(lf_template_2, 1, "bound")

        def_indef_template_text = [name_choices, VISUAL_VPS, "the", indef_choices, conj_statement, INTRANSITIVE_VPS_FOR_BOUND]
        def_indef_template_tags = ["np1", "vp1", None, "np2", None, "vp2"]
        def_indef_template = Template(def_indef_template_text, def_indef_template_tags)

        pairs += def_indef_template.generate(lf_template_1, 0, "bound")
        pairs += def_indef_template.generate(lf_template_2, 1, "bound")

        indef_indef_template_text = ["the", indef_choices, VISUAL_VPS, "the", indef_choices, conj_statement, INTRANSITIVE_VPS_FOR_BOUND]
        indef_indef_template_tags = [None, "np1", "vp1", None, "np2", None, "vp2"]
        indef_indef_template = Template(indef_indef_template_text, indef_indef_template_tags)

        pairs += indef_indef_template.generate(lf_template_1, 0, "bound")
        pairs += indef_indef_template.generate(lf_template_2, 1, "bound")

        return pairs

    if gender == "female":
        name_choices = FEMALE_NAMES
        indef_choices = INDEFINITE_FEMALE_NPS
        conj_statement = "and she"

        pairs = generate_animate(name_choices, indef_choices, conj_statement)

    elif gender == "male":
        name_choices = MALE_NAMES
        indef_choices = INDEFINITE_MALE_NPS
        conj_statement = "and he"

        pairs = generate_animate(name_choices, indef_choices, conj_statement)

    elif gender == "neuter":

        pairs = []

        indef_choices = INDEFINITE_NONHUMAN_SENTIENT_NPS
        conj_statement = "and it"

        indef_indef_template_text = ["the", indef_choices, VISUAL_VPS, "the", indef_choices, conj_statement, INTRANSITIVE_VPS_FOR_BOUND]
        indef_indef_template_tags = [None, "np1", "vp1", None, "np2", None, "vp2"]
        indef_indef_template = Template(indef_indef_template_text, indef_indef_template_tags)
        lf_template_1  = "{vp1} ( {np1}, {np2} ) AND {vp2} ( {np1} )" # it = np1
        lf_template_2  = "{vp1} ( {np1}, {np2} ) AND {vp2} ( {np2} )" # it = np2

        pairs += indef_indef_template.generate(lf_template_1, 0, "bound")
        pairs += indef_indef_template.generate(lf_template_2, 1, "bound")

    return pairs 



#NIEUWE MET TEMPLATE TYPE!!!!
#def generate_and_or_pairs():
    """
    Generate pairs of sentences with conjunction ambiguities
    of the form:
    "The man ate and drank or slept"
    """
    pairs = []

    # AND first template
    and_first_template_text = ["the", INDEFINITE_SENTIENT_NPS, INTRANSITIVE_VPS, "and", INTRANSITIVE_VPS, "or", INTRANSITIVE_VPS]
    and_first_template_tags = [None, "np1", "vp1", None, "vp2", None, "vp3"]
    and_first_template = Template(and_first_template_text, and_first_template_tags)

    and_first_lf_template_1 = "{vp1} ( {np1} ) AND ( {vp2} ( {np1} ) OR {vp3} ( {np1} ) )"
    and_first_lf_template_2 = "( {vp1} ( {np1} ) AND {vp2} ( {np1} ) ) OR {vp3} ( {np1} )"

    for pair in and_first_template.generate(and_first_lf_template_1, 0, "conj"):
        pair["template_type"] = "and_first"
        pairs.append(pair)
    for pair in and_first_template.generate(and_first_lf_template_2, 1, "conj"):
        pair["template_type"] = "and_first"
        pairs.append(pair)

    # OR first template
    or_first_template_text = ["the", INDEFINITE_SENTIENT_NPS, INTRANSITIVE_VPS, "or", INTRANSITIVE_VPS, "and", INTRANSITIVE_VPS]
    or_first_template_tags = [None, "np1", "vp1", None, "vp2", None, "vp3"]
    or_first_template = Template(or_first_template_text, or_first_template_tags)

    or_first_lf_template_1 = "{vp1} ( {np1} ) OR ( {vp2} ( {np1} ) AND {vp3} ( {np1} ) )"
    or_first_lf_template_2 = "( {vp1} ( {np1} ) OR {vp2} ( {np1} ) ) AND {vp3} ( {np1} )"

    for pair in or_first_template.generate(or_first_lf_template_1, 0, "conj"):
        pair["template_type"] = "or_first"
        pairs.append(pair)
    for pair in or_first_template.generate(or_first_lf_template_2, 1, "conj"):
        pair["template_type"] = "or_first"
        pairs.append(pair)

    return pairs

#WITH TRANSLATIONS
def generate_and_or_pairs():
    """
    Generate pairs of sentences with conjunction ambiguities
    of the form:
    "The man ate and drank or slept"
    """
    pairs = []

    and_first_template_text = ["the", INDEFINITE_SENTIENT_NPS, INTRANSITIVE_VPS, "and", INTRANSITIVE_VPS, "or", INTRANSITIVE_VPS]
    and_first_template_tags = [None, "np1", "vp1", None, "vp2", None, "vp3"]

    and_first_template = Template(and_first_template_text, and_first_template_tags)

    and_first_lf_template_1 = "{vp1} ( {np1} ) AND ( {vp2} ( {np1} ) OR {vp3} ( {np1} ) )"  # and binds first
    and_first_lf_template_2 = "( {vp1} ( {np1} ) AND {vp2} ( {np1} ) ) OR {vp3} ( {np1} )"  # or binds first

    # Generate pairs with translations for and_first template
    for i, (lf_template, idx) in enumerate([(and_first_lf_template_1, 0), (and_first_lf_template_2, 1)]):
        for pair in and_first_template.generate(lf_template, idx, "conj"):
            np1 = pair["var_bindings"]["np1"]
            vp1 = pair["var_bindings"]["vp1"]
            vp2 = pair["var_bindings"]["vp2"]
            vp3 = pair["var_bindings"]["vp3"]

            # Create translations based on the logical form
            if idx == 0:
                translation = (
                    f"The {np1} definitely {vp1}. And at least one of these two things happened: 1. The {np1} {vp2}. 2. The {np1} {vp3}."
                )
            else:
                translation = (
                    f"At least one of these two things happened: 1. The {np1} {vp1} and {vp2}. 2. The {np1} {vp3}."
                )

            pair["translation"] = translation
            pair["template_type"] = "and_first"
            pairs.append(pair)

    or_first_template_text = ["the", INDEFINITE_SENTIENT_NPS, INTRANSITIVE_VPS, "or", INTRANSITIVE_VPS, "and", INTRANSITIVE_VPS]
    or_first_template_tags = [None, "np1", "vp1", None, "vp2", None, "vp3"]

    or_first_template = Template(or_first_template_text, or_first_template_tags)

    or_first_lf_template_1 = "{vp1} ( {np1} ) OR ( {vp2} ( {np1} ) AND {vp3} ( {np1} ) )"  # or binds first
    or_first_lf_template_2 = "( {vp1} ( {np1} ) OR {vp2} ( {np1} ) ) AND {vp3} ( {np1} )"  # and binds first

    # Generate pairs with translations for or_first template
    for i, (lf_template, idx) in enumerate([(or_first_lf_template_1, 0), (or_first_lf_template_2, 1)]):
        for pair in or_first_template.generate(lf_template, idx, "conj"):
            np1 = pair["var_bindings"]["np1"]
            vp1 = pair["var_bindings"]["vp1"]
            vp2 = pair["var_bindings"]["vp2"]
            vp3 = pair["var_bindings"]["vp3"]

            # Create translations based on the logical form
            if idx == 0:
                translation = (
                    f"At least one of these two things happened: 1. The {np1} {vp1}. 2. The {np1} {vp2} and {vp3}."
                )
            else:
                translation = (
                    f"The {np1} definitely {vp3}. And at least one of these two things happened: 1. The {np1} {vp1}. 2. The {np1} {vp2}."
                )

            pair["translation"] = translation
            pair["template_type"] = "or_first"
            pairs.append(pair)

    return pairs

#WITH TRANSLATIONS
def generate_and_or_pairs_different_nps():
    """
    Generate pairs of sentences with conjunction ambiguities
    of the form:
    "The man ate and the woman drank or the dog slept"
    """
    pairs = []

    # AND binds first template
    and_first_template_text = ["the", INDEFINITE_SENTIENT_NPS, INTRANSITIVE_VPS, "and", "the", INDEFINITE_SENTIENT_NPS, INTRANSITIVE_VPS, "or", "the", INDEFINITE_SENTIENT_NPS, INTRANSITIVE_VPS]
    and_first_template_tags = [None, "np1", "vp1", None, None, "np2", "vp2", None, None, "np3", "vp3"]

    and_first_template = Template(and_first_template_text, and_first_template_tags)

    and_first_lf_template_1 = "{vp1} ( {np1} ) AND ( {vp2} ( {np2} ) OR {vp3} ( {np3} ) )"  # AND binds first
    and_first_lf_template_2 = "( {vp1} ( {np1} ) AND {vp2} ( {np2} ) ) OR {vp3} ( {np3} )"  # OR binds first

    for i, (lf_template, idx) in enumerate([(and_first_lf_template_1, 0), (and_first_lf_template_2, 1)]):
        for pair in and_first_template.generate(lf_template, idx, "conj"):
            np1 = pair["var_bindings"]["np1"]
            vp1 = pair["var_bindings"]["vp1"]
            np2 = pair["var_bindings"]["np2"]
            vp2 = pair["var_bindings"]["vp2"]
            np3 = pair["var_bindings"]["np3"]
            vp3 = pair["var_bindings"]["vp3"]

            # Create translations based on the logical form
            if idx == 0:
                translation = (
                    f"The {np1} definitely {vp1}. And at least one of these two things happened: 1. The {np2} {vp2}. 2. The {np3} {vp3}."
                )
            else:
                translation = (
                    f"At least one of these two things happened: 1. The {np1} {vp1} and the {np2} {vp2}. 2. The {np3} {vp3}."   
                )

            pair["translation"] = translation
            pair["template_type"] = "and_first"
            pairs.append(pair)

    # OR binds first template
    or_first_template_text = ["the", INDEFINITE_SENTIENT_NPS, INTRANSITIVE_VPS, "or", "the", INDEFINITE_SENTIENT_NPS, INTRANSITIVE_VPS, "and", "the", INDEFINITE_SENTIENT_NPS, INTRANSITIVE_VPS]
    or_first_template_tags = [None, "np1", "vp1", None, None, "np2", "vp2", None, None, "np3", "vp3"]

    or_first_template = Template(or_first_template_text, or_first_template_tags)

    or_first_lf_template_1 = "{vp1} ( {np1} ) OR ( {vp2} ( {np2} ) AND {vp3} ( {np3} ) )"  # OR binds first
    or_first_lf_template_2 = "( {vp1} ( {np1} ) OR {vp2} ( {np2} ) ) AND {vp3} ( {np3} )"  # AND binds first

    for i, (lf_template, idx) in enumerate([(or_first_lf_template_1, 0), (or_first_lf_template_2, 1)]):
        for pair in or_first_template.generate(lf_template, idx, "conj"):
            np1 = pair["var_bindings"]["np1"]
            vp1 = pair["var_bindings"]["vp1"]
            np2 = pair["var_bindings"]["np2"]
            vp2 = pair["var_bindings"]["vp2"]
            np3 = pair["var_bindings"]["np3"]
            vp3 = pair["var_bindings"]["vp3"]

            # Create translations based on the logical form
            if idx == 0:
                translation = (
                    f"At least one of these two things happened: 1. The {np1} {vp1}. 2. The {np2} {vp2} and the {np3} {vp3}."
                )
            else:
                translation = (
                    f"The {np3}  definitely {vp3}. And at least one of these two things happened: 1. The {np1} {vp1}. 2. The {np2} {vp2}."
                )

            pair["translation"] = translation
            pair["template_type"] = "or_first"
            pairs.append(pair)

    return pairs

#WITH TRANSLATIONS
def generate_iff_and_or_pairs_different_nps():
    """
    Generate pairs of sentences with conjunction ambiguities
    of the form:
    If the man ate the woman drank and the dog slept
        ( eat ( man ) IMPLY drink ( woman ) ) AND sleep ( dog )
        eat ( man ) IMPLY ( drink ( woman ) AND sleep ( dog ) )
    """
    pairs = []

    # IFF/ first template
    iff_first_template_text = [["if"], "the", INDEFINITE_SENTIENT_NPS, INTRANSITIVE_VPS, "the", INDEFINITE_SENTIENT_NPS, INTRANSITIVE_VPS, ["and"], "the", INDEFINITE_SENTIENT_NPS, INTRANSITIVE_VPS]
    iff_first_template_tags = ["conn1", None, "np1", "vp1", None, "np2", "vp2", "conn2", None, "np3", "vp3"]

    iff_first_template = Template(iff_first_template_text, iff_first_template_tags)

    iff_first_lf_template_1 = "{vp1} ( {np1} ) {conn1} ( {vp2} ( {np2} ) {conn2} {vp3} ( {np3} ) )"
    iff_first_lf_template_2 = "( {vp1} ( {np1} ) {conn1} {vp2} ( {np2} ) ) {conn2} {vp3} ( {np3} )"

    for i, (lf_template, idx) in enumerate([(iff_first_lf_template_1, 0), (iff_first_lf_template_2, 1)]):
        for pair in iff_first_template.generate(lf_template, idx, "conj"):
            np1 = pair["var_bindings"]["np1"]
            vp1 = pair["var_bindings"]["vp1"]
            np2 = pair["var_bindings"]["np2"]
            vp2 = pair["var_bindings"]["vp2"]
            np3 = pair["var_bindings"]["np3"]
            vp3 = pair["var_bindings"]["vp3"]

            # Create translations based on the logical form
            if idx == 0:
                translation = (
                    f"If the {np1} {vp1}, these two things happened: 1. The {np2} {vp2}. 2. The {np3} {vp3}."
                )
            else:
                translation = (
                    f"The {np3} definitely {vp3}. And if the {np1} {vp1}, this happened: 1. The {np2} {vp2}."   
                )

            pair["translation"] = translation
            pair["template_type"] = "iff_first"
            pairs.append(pair)

    # AND/OR first IFF template
    and_or_first_template_text = ["the", INDEFINITE_SENTIENT_NPS, INTRANSITIVE_VPS, ["and"], "the", INDEFINITE_SENTIENT_NPS, INTRANSITIVE_VPS, "if", "the", INDEFINITE_SENTIENT_NPS, INTRANSITIVE_VPS]
    and_or_first_template_tags = [None, "np1", "vp1", "conn1", None, "np2", "vp2", None, None, "np3", "vp3"]

    and_or_first_template = Template(and_or_first_template_text, and_or_first_template_tags)

    and_or_first_lf_template_1 = "{vp1} ( {np1} ) {conn1} ( {vp2} ( {np2} ) IMPLY {vp3} ( {np3} ) )"
    and_or_first_lf_template_2 = "( {vp1} ( {np1} ) {conn1} {vp2} ( {np2} ) ) IMPLY {vp3} ( {np3} )"

    for i, (lf_template, idx) in enumerate([(and_or_first_lf_template_1, 0), (and_or_first_lf_template_2, 1)]):
        for pair in and_or_first_template.generate(lf_template, idx, "conj"):
            np1 = pair["var_bindings"]["np1"]
            vp1 = pair["var_bindings"]["vp1"]
            np2 = pair["var_bindings"]["np2"]
            vp2 = pair["var_bindings"]["vp2"]
            np3 = pair["var_bindings"]["np3"]
            vp3 = pair["var_bindings"]["vp3"]

            # Create translations based on the logical form
            if idx == 0:
                translation = (
                    f"The {np1} definitely {vp1}. And if the {np3} {vp3}, this happened: 1. The {np2} {vp2}."
                )
            else:
                translation = (
                    f"If the {np3} {vp3}, these two things happened: 1. The {np1} {vp1} 2. the {np2} {vp2}. "   
                )

            pair["translation"] = translation
            pair["template_type"] = "and_or_first"
            pairs.append(pair)

    # # AND/OR first IMPLY template
    # and_or_first_if_template_text = ["the", INDEFINITE_SENTIENT_NPS, INTRANSITIVE_VPS, ["and", "or"], "the", INDEFINITE_SENTIENT_NPS, INTRANSITIVE_VPS, "if", "the", INDEFINITE_SENTIENT_NPS, INTRANSITIVE_VPS]
    # and_or_first_if_template_tags = [None, "np1", "vp1", "conn1", None, "np2", "vp2", None, None, "np3", "vp3"]

    # and_or_first_if_template = Template(and_or_first_if_template_text, and_or_first_if_template_tags)

    # and_or_first_if_lf_template_1 = "{vp3} ( {np3} ) IMPLY ( {vp1} ( {np1} ) {conn1} {vp2} ( {np2} ) )"
    # and_or_first_if_lf_template_2 = "{vp1} ( {np1} ) {conn1} ( {vp3} ( {np3} ) IMPLY {vp2} ( {np2} ) )"

    # for pair in and_or_first_if_template.generate(and_or_first_if_lf_template_1, 0, "conj"):
    #     pair["template_type"] = "and_or_first_if"
    #     pairs.append(pair)
    # for pair in and_or_first_if_template.generate(and_or_first_if_lf_template_2, 1, "conj"):
    #     pair["template_type"] = "and_or_first_if"
    #     pairs.append(pair)

    return pairs

#WITH TRANSLATIONS
def generate_not_pairs_different_nps():
    """
    Generate pairs of sentences with conjunction ambiguities
    of the form:
    It is not the case that the man drank and the woman ate
        NOT drink ( man ) AND eat ( woman )
        NOT ( drink ( man ) AND eat ( woman ) )
    """
    pairs = []

    # NOT with conjunction template
    not_conj_template_text = ["it is not the case that", "the", INDEFINITE_SENTIENT_NPS, INTRANSITIVE_VPS, ["and"], "the", INDEFINITE_SENTIENT_NPS, INTRANSITIVE_VPS] #, "or", "only if"
    not_conj_template_tags = [None, None, "np1", "vp1", "conn1", None, "np2", "vp2"]

    not_conj_template = Template(not_conj_template_text, not_conj_template_tags)

    not_conj_lf_template_1 = "NOT ( {vp1} ( {np1} ) {conn1} {vp2} ( {np2} ) )"  # NOT binds first
    not_conj_lf_template_2 = "NOT {vp1} ( {np1} ) {conn1} {vp2} ( {np2} )"      # Conjunction binds first

    # Generate pairs with translations for conjunction template
    for i, (lf_template, idx) in enumerate([(not_conj_lf_template_1, 0), (not_conj_lf_template_2, 1)]):
        for pair in not_conj_template.generate(lf_template, idx, "conj"):
            np1 = pair["var_bindings"]["np1"]
            np2 = pair["var_bindings"]["np2"]
            vp1 = pair["var_bindings"]["vp1"]
            vp2 = pair["var_bindings"]["vp2"]

            # Create translations based on the logical form
            if idx == 0:
                translation = (
                    f"These two things did not both happen: 1. The {np1} {vp1}. 2. The {np2} {vp2}."
                )
            else:
                translation = (
                    f"This thing did not happen: 1. The {np1} {vp1}. This did happen: 2. The {np2} {vp2}."
                )

            pair["translation"] = translation
            pair["template_type"] = "conjunction"
            pairs.append(pair)

    # NOT with implication template
    not_if_template_text = ["it is not the case that", "the", INDEFINITE_SENTIENT_NPS, INTRANSITIVE_VPS, "if", "the", INDEFINITE_SENTIENT_NPS, INTRANSITIVE_VPS]
    not_if_template_tags = [None, None, "np1", "vp1", None, None, "np2", "vp2"]

    not_if_template = Template(not_if_template_text, not_if_template_tags)

    not_if_lf_template_1 = "NOT ( {vp2} ( {np2} ) IMPLY {vp1} ( {np1} ) )"  # NOT binds first (reversed logic)
    not_if_lf_template_2 = "{vp2} ( {np2} ) IMPLY NOT {vp1} ( {np1} )"      # Implication binds first (reversed logic)

    # Generate pairs with translations for implication template
    for i, (lf_template, idx) in enumerate([(not_if_lf_template_1, 0), (not_if_lf_template_2, 1)]):
        for pair in not_if_template.generate(lf_template, idx, "conj"):
            np1 = pair["var_bindings"]["np1"]
            np2 = pair["var_bindings"]["np2"]
            vp1 = pair["var_bindings"]["vp1"]
            vp2 = pair["var_bindings"]["vp2"]

            # Create translations based on the logical form
            if idx == 0:
                translation = (
                    f"It is not true that if the {np2} {vp2}, the {np1} {vp1}."
                )
            else:
                translation = (
                    f"If the {np2} {vp2}, this did not happen: 1. The {np1} {vp1}."
                )

            pair["translation"] = translation
            pair["template_type"] = "implication"
            pairs.append(pair)

    return pairs




if __name__ == "__main__":

    # connective precedence

    and_or_pairs = generate_and_or_pairs()
    and_or_pairs_nps = generate_and_or_pairs_different_nps()

    xor_pairs = generate_xor_pairs()
    xor_pairs_nps = generate_xor_pairs_different_nps()

    iff_and_or_pairs_nps = generate_iff_and_or_pairs_different_nps()

    not_pairs_nps = generate_not_pairs_different_nps()

    # scope

    scope_pairs = generate_scope_pairs()
    reverse_scope_pairs = generate_reverse_scope_pairs()

    # bound pronouns

    # male_bound_pairs = generate_bound_pronoun_pairs("male")
    # female_bound_pairs = generate_bound_pronoun_pairs("female")
    # neuter_bound_pairs = generate_bound_pronoun_pairs("neuter")

    # bound_pairs = male_bound_pairs + female_bound_pairs + neuter_bound_pairs


    all_data = and_or_pairs + and_or_pairs_nps + xor_pairs + xor_pairs_nps + iff_and_or_pairs_nps + not_pairs_nps + scope_pairs + reverse_scope_pairs #+bound_pairs

    ambiguity_types = {
        "Conjunction Precedence (and/or)": and_or_pairs,
        "Conjunction Precedence (and/or) alternative": and_or_pairs_nps,
        "Exclusive Or (xor)": xor_pairs,
        "Exclusive Or (xor) alternative": xor_pairs_nps,
        "If and Only If (iff)": iff_and_or_pairs_nps,
        "Negation (not)": not_pairs_nps,
        "Quantifier Scope": scope_pairs,
        "Reversed Quantifier Scope": reverse_scope_pairs,
        #"Bound Pronouns": bound_pairs,
    }



NUM_SENTENCES_PER_TYPE = 20  # Change this number to adjust sampling

print(f"{NUM_SENTENCES_PER_TYPE} random sentences with logical forms and translations for each ambiguity type:\n")
for ambiguity, pairs in ambiguity_types.items():
    print(f"{ambiguity}:")

    # Check if template_type exists in the data
    has_template_types = any("template_type" in pair for pair in pairs)

    if has_template_types:
        # Group sentences by their template type
        grouped_by_template = {}
        for pair in pairs:
            template_type = pair.get("template_type", "unknown")  # Use template_type as key
            if template_type not in grouped_by_template:
                grouped_by_template[template_type] = {}

            # Group by surface for collecting all logical forms for the same sentence
            surface = pair["surface"]
            if surface not in grouped_by_template[template_type]:
                grouped_by_template[template_type][surface] = []
            grouped_by_template[template_type][surface].append((pair["lf"], pair.get("translation", "No translation available")))

        # For each template type, shuffle and select NUM_SENTENCES_PER_TYPE // 2 sentences
        num_per_template = NUM_SENTENCES_PER_TYPE // len(grouped_by_template)
        for template_type, template_sentences in grouped_by_template.items():
            print(f"  Template Type: {template_type}")
            random_sentences = list(template_sentences.items())
            random.shuffle(random_sentences)
            selected_sentences = random_sentences[:num_per_template]

            # Print the selected sentences, their logical forms, and translations
            for i, (sentence, lf_translation_pairs) in enumerate(selected_sentences):
                print(f"    Sentence {i + 1}: {sentence}")
                for j, (lf, translation) in enumerate(lf_translation_pairs):
                    print(f"      Logical Form {j + 1}: {lf}")
                    print(f"{translation}")
            print("-" * 20)

    else:
        # No template types, group by surface only
        grouped_pairs = {}
        for pair in pairs:
            surface = pair['surface']
            lf = pair['lf']
            translation = pair.get("translation", "No translation available")
            if surface not in grouped_pairs:
                grouped_pairs[surface] = []
            grouped_pairs[surface].append((lf, translation))

        # Shuffle and select NUM_SENTENCES_PER_TYPE sentences
        random_sentences = list(grouped_pairs.items())
        random.shuffle(random_sentences)
        selected_sentences = random_sentences[:NUM_SENTENCES_PER_TYPE]

        # Print the selected sentences, their logical forms, and translations
        for i, (sentence, lf_translation_pairs) in enumerate(selected_sentences):
            print(f"    Sentence {i + 1}: {sentence}")
            for j, (lf, translation) in enumerate(lf_translation_pairs):
                print(f"      Logical Form {j + 1}: {lf}")
                print(f"{translation}")
        print("-" * 20)

# Calculate and print the total number of sentences generated
total_sentences = sum(len(pairs) for pairs in ambiguity_types.values())
print(f"\nTotal number of sentences generated: {total_sentences}")

